import pandas as pd
import os
import re

def clean_stock_code(code):
    """
    處理代號欄位，保留有效的數字部分並加上 ".TW" 字樣。
    """
    if isinstance(code, str):
        match = re.search(r'(\d+)', code)
        if match:
            return match.group(0) + ".TW"  # 保留代號並加上 ".TW"
    return None  # 如果無法匹配，返回 None 以過濾掉無效值

def clean_market_cap(value):
    """
    處理市值欄位，移除千分位符號並轉換為浮點數。
    """
    if isinstance(value, str):
        value = value.replace(',', '')
        match = re.search(r'(\d+(?:\.\d+)?)', value)
        if match:
            return float(match.group(1))
    elif isinstance(value, (float, int)):
        return value
    return 0.0

def process_single_file(file_path):
    """
    處理單個CSV檔案，進行必要的欄位清理和轉換，確保數據有效性。
    """
    # 讀取CSV檔案
    df = pd.read_csv(
        file_path,
        header=0,  # 使用第一行作為表頭
    )
    
    # 清理"代號"欄位
    df['代號'] = df['代號'].apply(clean_stock_code)
    
    # 清理"市值(億)"欄位，轉換為浮點數
    df['市值(億)'] = df['市值(億)'].apply(clean_market_cap)
    
    # 選擇需要的欄位並去除缺失值及無效數據
    df = df[['產業別', '代號', '名稱', '市值(億)']].dropna(subset=['產業別', '代號', '市值(億)'])
    
    # 過濾掉市值為 0 的資料
    df = df[df['市值(億)'] > 0]
    
    return df

def aggregate_top_companies_by_sector(data_dir):
    """
    遍歷資料夾中的所有CSV檔案，合併數據並找出每個產業市值前三大的公司。
    """
    all_stocks = pd.DataFrame()

    # 遍歷資料夾中的所有CSV檔案
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_dir, filename)
            df = process_single_file(file_path)
            all_stocks = pd.concat([all_stocks, df], ignore_index=True)
    
    # 按產業別和市值排序
    sorted_df = all_stocks.sort_values(['產業別', '市值(億)'], ascending=[True, False])
    
    # 選擇每個產業市值前三大的公司
    result_df = pd.DataFrame(columns=['產業別', '代號', '名稱', '市值(億)'])
    for industry, industry_df in sorted_df.groupby('產業別'):
        top_3 = industry_df.head(3)[['產業別', '代號', '名稱', '市值(億)']]
        result_df = pd.concat([result_df, top_3], ignore_index=True)
    
    return result_df

def save_to_csv(df, output_file):
    """
    將DataFrame儲存為CSV檔案。
    """
    df.to_csv(output_file, index=False)
    print(f"CSV檔案已儲存到 {output_file}!")

# 使用函式
if __name__ == "__main__":
    data_dir = 'D:' + os.path.sep + 'AI_course' + os.path.sep + 'Finance_data_visualization' + os.path.sep + 'Finance-data-visualization'
    output_file = 'top_market_cap_by_sector.csv'

    # 處理財務數據並儲存結果
    result = aggregate_top_companies_by_sector(data_dir)
    save_to_csv(result, output_file)

    # 檢視前幾行結果
    print(result.head())
