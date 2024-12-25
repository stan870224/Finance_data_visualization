import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from modules.initialize_data.insert_sql import save_data_to_mssql
from modules.shared_params.param_config import DatabaseConnection, mssql_login_info

    
def get_api_key():
    with open('Finance_data_visualization\modules\initialize_data\config.json', 'r') as f:
        config = json.load(f)
        FRED_API_KEY = config['FRED_API_KEY']
    return FRED_API_KEY        

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

def save_policy_rate_to_mssql(policy_rate_df):
    """
    將政策利率數據存入 MSSQL
    """
    db_connection = DatabaseConnection(mssql_login_info)
    save_data_to_mssql(policy_rate_df, "Policy_Rate_Data", db_connection)


def save_cpi_to_mssql(cpi_df):
    """
    將 CPI 數據存入 MSSQL
    """
    db_connection = DatabaseConnection(mssql_login_info)
    save_data_to_mssql(cpi_df, "CPI_Data", db_connection)

