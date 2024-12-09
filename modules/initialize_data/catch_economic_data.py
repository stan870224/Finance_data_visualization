import json
import pandas as pd
import requests
from datetime import datetime, timedelta
import pyodbc  # 用於連接 MSSQL 資料庫

# 讀取配置文件
with open('modules/initialize_data/config.json', 'r') as f:
    config = json.load(f)
    FRED_API_KEY = config['FRED_API_KEY']

# MSSQL 資料庫配置
MSSQL_CONFIG = {
    "server": "YOUR_SERVER",
    "database": "YOUR_DATABASE",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

# 設定時間範圍
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')

def fetch_fred_data(series_id, start_date, end_date, api_key):
    """使用FRED REST API获取數據"""
    base_url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # 確保請求成功
    data = response.json()['observations']
    return pd.DataFrame(data)[['date', 'value']].rename(columns={'date': '日期', 'value': series_id})

def save_economic_data_to_mssql(df, table_name, mssql_config):
    """將 DataFrame 存入 MSSQL 資料库"""
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={mssql_config['server']};"
        f"DATABASE={mssql_config['database']};"
        f"UID={mssql_config['username']};"
        f"PWD={mssql_config['password']}"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 創建表（如果不存在）
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
    CREATE TABLE {table_name} (
        日期 NVARCHAR(50),
        數據1 NVARCHAR(50),
        數據2 NVARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    # 插入數據
    for index, row in df.iterrows():
        cursor.execute(
            f"INSERT INTO {table_name} (日期, 數據1, 數據2) VALUES (?, ?, ?)",
            row['日期'], row.iloc[1], row.iloc[2] if len(row) > 2 else None
        )
    conn.commit()
    conn.close()
    print(f"數據已保存至 MSSQL 表: {table_name}")

# 獲取政策利率數據
def get_policy_rate_data(start_date, end_date, api_key):
    upper_limit_df = fetch_fred_data('DFEDTARU', start_date, end_date, api_key)
    lower_limit_df = fetch_fred_data('DFEDTARL', start_date, end_date, api_key)

    # 合併上下限的目標區間
    policy_rate_df = pd.merge(upper_limit_df, lower_limit_df, on='日期', how='outer')
    policy_rate_df.rename(columns={'DFEDTARU': '目標利率上限', 'DFEDTARL': '目標利率下限'}, inplace=True)

    # 計算政策利率（目標區間的中間值）
    policy_rate_df['政策利率'] = (pd.to_numeric(policy_rate_df['目標利率上限'], errors='coerce') +
                                pd.to_numeric(policy_rate_df['目標利率下限'], errors='coerce')) / 2

    return policy_rate_df

# 獲取 CPI 數據 改成計算年增率四捨五入至小數後1位
def get_cpi_data(start_date, end_date, api_key):
    cpi_df = fetch_fred_data('CPIAUCSL', start_date, end_date, api_key)
    cpi_df['CPIAUCSL'] = pd.to_numeric(cpi_df['CPIAUCSL'], errors='coerce')

    # 計算月通貨膨脹率
    cpi_df = cpi_df.sort_values('日期')
    cpi_df['月通貨膨脹率'] = cpi_df['CPIAUCSL'].pct_change() * 100

    return cpi_df

# 主程式
def main():
    try:
        # 獲取政策利率數據
        policy_rate_df = get_policy_rate_data(start_date, end_date, FRED_API_KEY)
        save_economic_data_to_mssql(policy_rate_df, "PolicyRateTable", MSSQL_CONFIG)

        # 獲取 CPI 數據
        cpi_df = get_cpi_data(start_date, end_date, FRED_API_KEY)
        save_economic_data_to_mssql(cpi_df, "CpiTable", MSSQL_CONFIG)

    except Exception as e:
        print(f"程式執行過程發生錯誤: {e}")

if __name__ == "__main__":
    main()
