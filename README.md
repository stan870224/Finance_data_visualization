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
1. **數據準備與清理**
   - 確保數據完整性與準確性：包括股票名稱、利率變化、日期、漲跌幅等欄位
   - 使用`pandas`進行數據讀取與清洗：處理缺失值、格式轉換及數據篩選

2. **美聯儲利率數據**
   - 格式：CSV/JSON
   - 清理：統一日期格式、處理缺失值

3. **台股股價數據**
   - 頻率：日K線資料

4. **資料驗證**
   - 檢查時間區間完整性
   - 確認股票代碼正確性
   - 驗證利率公布日期準確性

### 第二階段：數據處理與計算
1. **時間對齊**
   - 處理非交易日問題
   - 建立利率公布日與股價日期的對應關係

2. **計算股價反應指標**
   - 月線反應
   - 類股平均

3. **相關性分析**
   - 利率變動幅度 vs 股價反應
   - 升息 vs 降息的不同影響

### 第三階段：視覺化開發
1. **圖表設計與實現**
   - **時間序列圖**
     - 顯示美聯儲公布利率後，各類股漲跌幅的變化趨勢
     - X軸為日期，Y軸為漲跌幅，分類別顏色標註不同的類股（例如科技、金融、能源等）
     - 使用`matplotlib`或`seaborn`繪製折線圖，添加標記點凸顯利率公布日期
   
   - **箱型圖**
     - 分析利率公布後各類股的漲跌幅分布情況，展示不同類股的波動範圍與中位數
     - 使用`seaborn`的`boxplot`功能進行繪製
   
   - **相關性熱力圖**
     - 探索利率變化與各類股表現之間的相關性
     - 使用`seaborn`的`heatmap`展示相關性矩陣
   
   - **柱狀圖**
     - 顯示利率高於預期、低於預期和符合預期時，各類股的平均漲跌幅
     - 使用`matplotlib`或`seaborn`的`barplot`功能進行實現

2. **視覺化美化與標註**
   - 添加標題、軸標籤及圖例，使圖表更具可讀性
   - 在關鍵點（如利率公布日期或極值點）添加標註，提升圖表信息量
   - 使用配色方案區分不同類股或情境（高於、低於、符合預期）

3. **時間序列圖表**
   - 利率走勢線圖
   - 各類股指數走勢
   - 重要利率決策點標記

4. **相關性分析圖表**

5. **互動式儀表板**
   - 詳細數據展示

## 預期產出
1. 完整的資料處理管道
2. 互動式分析儀表板
3. 各類股與利率相關性報告
4. 可重複使用的分析模板

## 注意事項
1. 需要處理台股除權除息對股價的影響
2. 美聯儲利率公布時間與台股交易時間差異
3. 需考慮其他重大事件對股價的影響
4. 確保數據的即時性和準確性