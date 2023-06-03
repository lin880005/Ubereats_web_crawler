from selenium import webdriver # 瀏覽器
from selenium.webdriver.common.by import By # 選取器
from selenium.webdriver.support.wait import WebDriverWait # 網站等待
from selenium.webdriver.support import expected_conditions as EC # 元素狀態判斷
from selenium.webdriver.chrome.options import Options
import time
import openpyxl
import re

wb = openpyxl.Workbook()
ws = wb.active

ws["A1"] = "URL"


options = Options()
options.add_argument("--disable-notifications") # 關閉彈出式視窗
driver = webdriver.Chrome(chrome_options = options)

driver.get("https://www.ubereats.com/tw")

# 在首頁輸入地址
getblock = driver.find_element(By.XPATH, '//*[@placeholder="輸入外送地址"]')
getblock.send_keys('高雄市')
time.sleep(1)
getblock.send_keys('\ue007') # 按下Enter
time.sleep(3)

# 點下熱門餐點radio button，為了先進一步排除前幾類自動推薦的餐廳(排列順序太雜亂不好爬)
rating = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="  熱門餐點"]')))
rating.click()
time.sleep(5)

while True: 
    try: 
        more = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="顯示更多餐廳"]')))
        more.click()
        time.sleep(6)
    except: 
        break

# 定位餐廳網址
stores = driver.find_elements(By.XPATH, '//a[@data-testid="store-card"]')
count = 0

for store_url in stores:
    restaurant_url = store_url.get_attribute("href")
    time.sleep(1)
    count+=1
    print(f"====第{count}間====")
    ws.append([restaurant_url])
    wb.save("Uber_eats高雄市餐廳網址.xlsx")

driver.quit()


