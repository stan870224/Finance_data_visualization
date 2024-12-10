import pandas as pd
import yfinance as yf

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





