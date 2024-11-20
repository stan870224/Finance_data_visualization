import pandas as pd
import yfinance as yf
import pyodbc
import os
from datetime import datetime, timedelta


def fetch_stock_codes(input_file):
    """
    從 CSV 文件中讀取所有代號並存入列表。

    Args:
        input_file (str): CSV 文件路徑。

    Returns:
        list: 代號列表。
    """
    if not input_file.endswith('.csv') or not pd.io.common.file_exists(input_file):
        raise FileNotFoundError(f"找不到文件：{input_file}")

    # 讀取 CSV，獲取代號
    df = pd.read_csv(input_file)
    df['代號'] = df['代號'].apply(lambda x: str(
        x) if pd.notnull(x) else x)  # 確保代號是字串
    codes = df['代號'].dropna().unique().tolist()
    print(f"共讀取 {len(codes)} 個股票代號。")
    return codes


def fetch_historical_data(stock_codes, start_date, end_date):
    """
    使用 yfinance 獲取股票的歷史數據並清理髒資料。

    Args:
        stock_codes (list): 股票代號列表 (包含 .TW 後綴)。
        start_date (str): 起始日期，格式 'YYYY-MM-DD'。
        end_date (str): 結束日期，格式 'YYYY-MM-DD'。

    Returns:
        pd.DataFrame: 清理後的歷史數據。
    """
    # 初始化空的 DataFrame 存儲所有股票的數據
    all_data = pd.DataFrame()

    # 遍歷股票代號列表，逐個下載數據
    for code in stock_codes:
        try:
            # 使用 yfinance 獲取股票歷史數據
            stock = yf.Ticker(code)
            stock_data = stock.history(start=start_date, end=end_date)

            # 重設索引並重命名日期列
            stock_data.reset_index(inplace=True)

            # 添加股票代碼列以識別不同股票
            stock_data['Stock_Code'] = code

            # 選取指定的欄位
            stock_data = stock_data[[
                'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Stock_Code']]

            # 清理髒資料：去除缺失值，重設索引
            stock_data.dropna(inplace=True)

            # 合併到總的 DataFrame
            all_data = pd.concat([all_data, stock_data], ignore_index=True)

        except Exception as e:
            print(f"Error fetching data for {code}: {e}")

    return all_data


def save_to_mssql(data, table_name, server, database, username, password):
    """
    將 DataFrame 存入 MSSQL 資料庫，使用 SQL Server 驗證。

    Args:
        data (pd.DataFrame): 要存入的數據。
        table_name (str): 資料表名稱。
        server (str): MSSQL 伺服器名稱或 IP。
        database (str): 資料庫名稱。
        username (str): SQL Server 帳號。
        password (str): SQL Server 密碼。
    """
    conn = None
    try:
        # 使用 SQL Server 驗證連接 MSSQL
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        cursor = conn.cursor()

        # 創建資料表（如果不存在）
        cursor.execute(f"""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
        CREATE TABLE {table_name} (
            [Trading_Date] DATE,
            [Open_Price] FLOAT,
            [High_Price] FLOAT,
            [Low_Price] FLOAT,
            [Close_Price] FLOAT,
            [Trading_Volume] BIGINT,
            [Stock_Code] VARCHAR(50)
        )
        """)



        for index, row_data in data.iterrows():
            try:
                cursor.execute(
                    "INSERT INTO " + table_name + 
                    " ([Trading_Date],[Open_Price],[High_Price],[Low_Price],[Close_Price],[Trading_Volume],[Stock_Code]) " +
                    "VALUES (?,?,?,?,?,?,?)",
                    (
                        row_data['Date'].date(), 
                        float(row_data['Open']), 
                        float(row_data['High']), 
                        float(row_data['Low']), 
                        float(row_data['Close']), 
                        int(row_data['Volume']), 
                        str(row_data['Stock_Code'])
                    )
                )
            except Exception as e:
                print(f"插入數據時發生錯誤: {str(e)}")
                print(f"錯誤數據: {row_data}")
                continue

        conn.commit()
        print(f"成功將數據存入資料表 {table_name}！")

    except Exception as e:
        print(f"儲存數據到 MSSQL 時發生錯誤: {str(e)}")
        raise
    finally:
        if conn is not None:
            conn.close()

# 主程式

"""
def main():
    file_path = 'D:' + os.path.sep + 'AI_course' + os.path.sep + 'Finance_data_visualization' + os.path.sep + 'Finance_data_visualization' + os.path.sep +'top_market_cap_by_sector'
    input_file = os.path.join(file_path,'top_market_cap_by_sector.csv')
    table_name = 'Stock_Historical_Data'
    server, database, username, password = mssql_login_info()
    

    # 設定查詢範圍為過去十年
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365*10)
                  ).strftime('%Y-%m-%d')

    # 取得代號列表
    stock_codes = fetch_stock_codes(input_file)

    # 獲取歷史數據
    historical_data = fetch_historical_data(stock_codes, start_date, end_date)

    # 儲存至 MSSQL
    save_to_mssql(historical_data, table_name, server, database, username, password)


# 執行主程式
if __name__ == '__main__':
    main()

"""