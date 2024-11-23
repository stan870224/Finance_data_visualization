# Finance-data-visualization
 The goal is to apply Python data analysis libraries to visualize the performance of various Taiwanese stock sectors following the Federal Reserve's interest rate announcement.

project_directory/
│
├── data/                     # 原始數據與處理後數據存放目錄
│   ├── raw/                  # 原始數據
│   ├── processed/            # 處理後數據
│
├── modules/
│   ├── initialize_data/      # 初始化數據的模組
│   │   ├── __init__.py       # 模組初始化文件
│   │   └── init_processor.py # 處理初始化數據
│   │
│   ├── daily_update/         # 每日更新的模組
│   │   ├── __init__.py       # 模組初始化文件
│   │   └── daily_processor.py # 每日資料處理
│   │
│   ├── data_visualization/   # 數據視覺化的模組
│       ├── __init__.py       # 模組初始化文件
│       └── visualizer.py     # 數據視覺化處理
│
├── main.py                   # 主程式入口
├── requirements.txt          # 所需的 Python library
└── README.md                 # 專案說明文件


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