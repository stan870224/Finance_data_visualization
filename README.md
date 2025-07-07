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
    ├── 📂 daily_update                 # 每日數據更新模組
    │
    ├── 📂 data_visualization           # 數據視覺化模組
    │
    ├── 📂 initialize_data              # 初始化數據模組
    │   ├── 📄 catch_finance_web_info.py # 抓取財務數據邏輯
    │   ├── 📄 data_save_func.py        # 資料保存路徑函數
    │   ├── 📄 finance_catch.py         # 財務數據清理與處理
    │   ├── 📄 finance_catch_10y.py     # 抓取十年歷史財務數據
    │   ├── 📄 insert_sql.py            # 儲存數據到 MSSQL
    │
    ├── 📂 shared_params                # 共用參數模組
        ├── 📄 __init__.py              # 初始化文件
        ├── 📄 param_config.py          # 資料庫連線與配置
 




# 台股與美聯儲利率相關性分析專案架構

## 專案目標
分析台灣股市各類股龍頭與美聯儲利率政策的相關性，透過十年數據建立視覺化分析系統

## 核心數據需求

### 1. 美聯儲利率數據 (FED Rate Table)
- **時間範圍**: 2015-2025 (十年數據)
- **數據欄位**:
  - 利率公布日期
  - 公布利率 (%)
  - 利率變動幅度 (升息/降息)
  - 會議類型 (定期/緊急)

### 2. 台股各類股龍頭股票數據
- **股票選擇標準**: 各類股市值前三大


### 3. 股價反應數據表 (Price Reaction Table)
- **時間節點**:
  - 利率公布當天收盤價
  - 利率公布隔天開盤價
  - 利率公布後一個月收盤價
- **計算指標**:
  - 隔日開盤反應 (%)
  - 一個月累積漲跌幅 (%)
  - 各類股平均漲跌幅 (三檔股票平均)

## 執行步驟詳細規劃

### 第一階段：資料蒐集與整理
1. **美聯儲利率數據**
   - 格式：CSV/JSON
   - 清理：統一日期格式、處理缺失值

2. **台股股價數據**
   - 頻率：日K線資料

3. **資料驗證**
   - 檢查時間區間完整性
   - 確認股票代碼正確性
   - 驗證利率公布日期準確性



### 第二階段：數據處理與計算
1. **時間對齊**
   - 處理非交易日問題
   - 建立利率公布日與股價日期的對應關係

2. **計算股價反應指標**
   - 隔日開盤反應 = (隔日開盤價 - 當日收盤價) / 當日收盤價
   - 月線反應 = (一個月後收盤價 - 當日收盤價) / 當日收盤價
   - 類股平均 = (股票A + 股票B + 股票C) / 3

3. **相關性分析**
   - 利率變動幅度 vs 股價反應
   - 升息 vs 降息的不同影響

### 第三階段：視覺化開發
1. **時間序列圖表**
   - 利率走勢線圖
   - 各類股指數走勢
   - 重要利率決策點標記

2. **相關性分析圖表**

3. **互動式儀表板**
   - 詳細數據展示



## 預期產出
1. 完整的資料處理管道
2. 互動式分析儀表板
3. 各類股與利率相關性報告
4. 可重複使用的分析模板


## 注意事項
1. 需要處理台股除權除息對股價的影響
2. 美聯儲利率公布時間與台股交易時間差異
3. 需考虑其他重大事件對股價的影響
4. 確保數據的即時性和準確性