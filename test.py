import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# 發送 HTTP GET 請求並取得網頁內容
url = 'https://www.ubereats.com'
response = requests.get(url)

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 找到餐廳的容器元素
restaurants = soup.find_all('div', class_='restaurant')

# 儲存餐廳資訊的清單
restaurant_list = []

# 逐一解析每個餐廳元素，提取所需的資訊
for restaurant in restaurants:
    name = restaurant.find('h1', class_='restaurant-name').text.strip()
    address = restaurant.find('div', class_='restaurant-location').text.strip()
    rating = restaurant.find('div', class_='star-rating').get('aria-label')
    restaurant_list.append({'Name': name, 'Address': address, 'Rating': rating})

# 將餐廳資訊轉換為 DataFrame
df = pd.DataFrame(restaurant_list)

# 儲存 DataFrame 為 Excel 檔案
df.to_excel('ubereats_restaurants.xlsx', index=False)