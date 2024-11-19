import yfinance as yf
from datetime import datetime, timedelta
import Finance_Catch_10y as fi
import pandas as pd


end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365*10)).strftime('%Y-%m-%d')
stock_code = ['1210.TW','2330.TW']

historical_data = fi.fetch_historical_data(stock_code, start_date, end_date)

df = pd.DataFrame(historical_data)

# 將 DataFrame 儲存為 CSV 檔案
df.to_csv('stock_data.csv', index=False, encoding='utf-8-sig')

print("資料已儲存為 CSV 檔案 stock_data.csv")