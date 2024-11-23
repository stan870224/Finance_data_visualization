from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 初始化 Selenium 瀏覽器
driver = webdriver.Chrome()

# 打開目標網站
url = "https://hk.investing.com/economic-calendar/interest-rate-decision-168"
driver.get(url)

# 等待頁面加載
time.sleep(5)

# 嘗試點擊關閉彈窗的按鈕
try:
    close_icon = driver.find_element(By.CLASS_NAME, "popupCloseIcon.largeBannerCloser")
    close_icon.click()
    print("彈窗已成功關閉")
except Exception as e:
    print("未找到彈窗按鈕，或者已自動關閉:", e)

# 接下來可以繼續撰寫爬取邏輯
time.sleep(5)  # 等待操作完成
driver.quit()
