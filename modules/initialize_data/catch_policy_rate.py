import json

import pandas as pd
import requests

# 指定 config.json 的路徑
config_file_path = "config.json"  # 或 "/完整/路徑/到/config.json"

# 讀取配置文件
try:
    with open(config_file_path, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"配置文件未找到，請確認路徑: {config_file_path}")

# 獲取 API Key
API_KEY = config.get("TRADINGECONOMICS_API_KEY")
if not API_KEY:
    raise ValueError("配置文件中未設置 TRADINGECONOMICS_API_KEY")

# Trading Economics API 配置
BASE_URL = "https://api.tradingeconomics.com"

# 請求利率數據的 API
endpoint = f"{BASE_URL}/historical/country/united states/indicator/interest rate"
params = {
    "c": API_KEY,  # API Key
    "f": "json"    # 返回格式
}

# 發送 API 請求
try:
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # 確保請求成功
    data = response.json()  # 解析 JSON 響應
except requests.exceptions.RequestException as e:
    print(f"請求失敗: {e}")
    exit()

# 解析數據
parsed_data = []
for record in data:
    parsed_data.append({
        "日期": record.get("date"),
        "實際值": record.get("actual"),
        "預測": record.get("forecast"),
        "前值": record.get("previous")
    })

# 將數據轉為 DataFrame
df = pd.DataFrame(parsed_data)

# 保存為 CSV 文件
output_file = "tradingeconomics_interest_rate.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"數據已保存至: {output_file}")
