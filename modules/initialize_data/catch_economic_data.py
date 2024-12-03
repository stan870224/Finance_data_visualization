import json
import pandas as pd
import requests
from datetime import datetime, timedelta
import pyodbc  # 用于连接 MSSQL 数据库

# 读取配置文件
with open('modules/initialize_data/config.json', 'r') as f:
    config = json.load(f)
    FRED_API_KEY = config['FRED_API_KEY']

# MSSQL 数据库配置
MSSQL_CONFIG = {
    "server": "YOUR_SERVER",
    "database": "YOUR_DATABASE",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

# 设置时间范围
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')

def fetch_fred_data(series_id, start_date, end_date, api_key):
    """使用FRED REST API获取数据"""
    base_url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # 确保请求成功
    data = response.json()['observations']
    return pd.DataFrame(data)[['date', 'value']].rename(columns={'date': '日期', 'value': series_id})

def save_to_mssql(df, table_name, mssql_config):
    """将 DataFrame 存入 MSSQL 数据库"""
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={mssql_config['server']};"
        f"DATABASE={mssql_config['database']};"
        f"UID={mssql_config['username']};"
        f"PWD={mssql_config['password']}"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
    CREATE TABLE {table_name} (
        日期 NVARCHAR(50),
        数据1 NVARCHAR(50),
        数据2 NVARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    # 插入数据
    for index, row in df.iterrows():
        cursor.execute(
            f"INSERT INTO {table_name} (日期, 数据1, 数据2) VALUES (?, ?, ?)",
            row['日期'], row.iloc[1], row.iloc[2] if len(row) > 2 else None
        )
    conn.commit()
    conn.close()
    print(f"数据已保存至 MSSQL 表: {table_name}")

# 获取政策利率数据
def get_policy_rate_data(start_date, end_date, api_key):
    upper_limit_df = fetch_fred_data('DFEDTARU', start_date, end_date, api_key)
    lower_limit_df = fetch_fred_data('DFEDTARL', start_date, end_date, api_key)

    # 合并上下限目标区间
    policy_rate_df = pd.merge(upper_limit_df, lower_limit_df, on='日期', how='outer')
    policy_rate_df.rename(columns={'DFEDTARU': '目标利率上限', 'DFEDTARL': '目标利率下限'}, inplace=True)

    # 计算政策利率（目标区间的中值）
    policy_rate_df['政策利率'] = (pd.to_numeric(policy_rate_df['目标利率上限'], errors='coerce') +
                                pd.to_numeric(policy_rate_df['目标利率下限'], errors='coerce')) / 2

    return policy_rate_df

# 获取 CPI 数据
def get_cpi_data(start_date, end_date, api_key):
    cpi_df = fetch_fred_data('CPIAUCSL', start_date, end_date, api_key)
    cpi_df['CPIAUCSL'] = pd.to_numeric(cpi_df['CPIAUCSL'], errors='coerce')

    # 计算月通胀率
    cpi_df = cpi_df.sort_values('日期')
    cpi_df['月通胀率'] = cpi_df['CPIAUCSL'].pct_change() * 100

    return cpi_df

# 主程序
def main():
    try:
        # 获取政策利率数据
        policy_rate_df = get_policy_rate_data(start_date, end_date, FRED_API_KEY)
        save_to_mssql(policy_rate_df, "PolicyRateTable", MSSQL_CONFIG)

        # 获取 CPI 数据
        cpi_df = get_cpi_data(start_date, end_date, FRED_API_KEY)
        save_to_mssql(cpi_df, "CpiTable", MSSQL_CONFIG)

    except Exception as e:
        print(f"程序执行过程中出现错误: {e}")

if __name__ == "__main__":
    main()
