from datetime import datetime, timedelta
from modules.initialize_data.data_save_func import data_save
from modules.initialize_data.finance_catch import aggregate_top_companies_by_sector, save_to_csv
from modules.initialize_data.finance_catch_10y import fetch_historical_data, fetch_stock_codes, save_to_mssql
from modules.initialize_data.sql_login_info import mssql_login_info

def main():
    data_dir, file_path, output_file, input_file, table_name = data_save()
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

    # 處理財務數據並儲存結果
    result = aggregate_top_companies_by_sector(data_dir)
    save_to_csv(result, output_file)
    # 檢視前幾行結果
    print(result.head())
    
if __name__ == "__main__":
    main()
        