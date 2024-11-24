# Finance-data-visualization
 The goal is to apply Python data analysis libraries to visualize the performance of various Taiwanese stock sectors following the Federal Reserve's interest rate announcement.

# Project Directory Structure

This document outlines the structure of the project directory and the purpose of each file and folder.

```plaintext
Finance_data_visualization/
│
├── 📄 README.md                        # 專案說明文件
│
├── 📂 data                             # 數據存放目錄
│   ├── 📂 processed_data               # 處理後數據
│   │
│   ├── 📂 row_data                     # 原始數據
│
├── 📄 main.py                          # 主程式入口
│
├── 📂 modules                          # 功能模組
│   ├── 📂 daily_update                 # 每日數據更新模組
│   │
│   ├── 📂 data_visualization           # 數據視覺化模組
│   │
│   ├── 📂 initialize_data              # 初始化數據模組
│   │   ├── 📄 catch_finance_web_info.py # 抓取財務數據邏輯
│   │   ├── 📄 data_save_func.py        # 資料保存路徑函數
│   │   ├── 📄 finance_catch.py         # 財務數據清理與處理
│   │   ├── 📄 finance_catch_10y.py     # 抓取十年歷史財務數據
│   │   ├── 📄 insert_sql.py            # 儲存數據到 MSSQL
│   │
│   ├── 📂 shared_params                # 共用參數模組
│       ├── 📄 __init__.py              # 初始化文件
│       ├── 📄 param_config.py          # 資料庫連線與配置
│




執行步驟 :
1.取得十年台股前三大龍頭股及十年美聯儲升降息數據
2.清理資料轉入資料庫
3.將資料視覺化

十年數據 

開table FED 利率


開table
利率公布時間 2023/1
各類股名稱(抓取各類股前三龍頭)
美聯儲公布利率為低於預期或高於預期 -1 0 1
公布利率後隔天開盤價
公布利率後一個月收盤價
公布利率後之漲跌幅