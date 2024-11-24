from datetime import datetime, timedelta
from modules.initialize_data.data_save_func import data_save
from modules.initialize_data.finance_catch import (
    aggregate_top_companies_by_sector,
    save_to_csv
)
from modules.initialize_data.finance_catch_10y import (
    fetch_historical_data,
    fetch_stock_codes
)
from modules.initialize_data.insert_sql import save_stock_data_to_mssql
from modules.shared_params.param_config import DatabaseConnection, mssql_login_info
import os


def main():
    # 1. 取得資料保存相關路徑和表名
    data_dir, file_path, output_file, input_file, table_name = data_save()

    # 檢查資料夾是否存在
    if not os.path.exists(data_dir):
        print(f"資料夾 {data_dir} 不存在，請檢查路徑。")
        return

    # 2. 處理財務數據，找出市值前三大的公司
    print("正在處理財務數據...")
    result = aggregate_top_companies_by_sector(data_dir)
    print("財務數據處理完成。")

    # 3. 保存結果到 CSV 文件
    print(f"正在將結果保存到文件：{output_file}")
    save_to_csv(result, output_file)
    print("數據保存完成。")

    # 4. 設定查詢範圍為過去十年
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')

    # 5. 獲取股票代號列表
    stock_codes = fetch_stock_codes(input_file)
    if not stock_codes:
        print("無法獲取股票代號列表，請檢查輸入檔案。")
        return

    # 6. 獲取歷史數據
    print(f"開始獲取歷史數據（{start_date} 至 {end_date}）...")
    historical_data = fetch_historical_data(stock_codes, start_date, end_date)
    if historical_data.empty:
        print("無法獲取歷史數據，請檢查網絡或資料來源。")
        return
    print("歷史數據獲取完成。")

    # 7. 儲存歷史數據到 MSSQL
    print("開始將數據儲存至 MSSQL...")
    db_connection = DatabaseConnection(mssql_login_info)
    try:
        save_stock_data_to_mssql(historical_data, table_name, db_connection)
    finally:
        db_connection.close()
    print("數據儲存至 MSSQL 完成。")

    # 8. 顯示結果預覽
    print("結果預覽：")
    print(result.head())


if __name__ == "__main__":
    main()
