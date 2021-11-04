# import du lieu
from os import pipe
import sys
from requests.api import request 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import re

import requests
import bs4
from bs4 import BeautifulSoup
import json

# Option
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome();

# BASE_URL
BASE_URL = [
    'https://tiki.vn/bestsellers-2020/dien-thoai-may-tinh-bang/c1789',
    'https://tiki.vn/bestsellers-2020/dien-thoai-may-tinh-bang/c1789?p=2',
    'https://tiki.vn/bestsellers-2020/dien-thoai-may-tinh-bang/c1789?p=3',
    'https://tiki.vn/bestsellers-2020/dien-thoai-may-tinh-bang/c1789?p=4'
]

comment_list = []
for i in range(len(BASE_URL)):
    # Open website
    browser.get(BASE_URL[i])

    sleep(2)

    # Get page source
    page_source = BeautifulSoup(browser.page_source)

    # Get Link of Product
    link_phone_list = []
    for link in page_source.select('p.title a[href]'):
        link_phone_list.append(link['href'])

    # Get Product id of each Product with re
    product_id_list = []
    for i in range(len(link_phone_list)):
        txt = link_phone_list[i]
        product_id = re.findall("p\d{1,10}", txt)
        product_id = re.sub("p","", product_id[0])
        product_id_list.append(product_id)

    # Get data from api
    def getData(url):    
        print("API:", url)
        header = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            data = response.json()['data']         
            for i in range(len(data)):
                if (data[i]['content'] and data[i]['rating']):                      
                    comment_list.append({"content":data[i]['content'],"rating":data[i]['rating']})
            print("Is crawl:", len(comment_list) , " comments")
        else:
            print("Time out connect")

    # Loop product id
    for i in range(len(product_id_list)):
        print("\n================================================")
        product_id = product_id_list[i]     
        print("Crawling Product Id:", product_id)
        api_url = f"https://tiki.vn/api/v2/reviews?limit=500&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page=1&product_id={product_id}"
        getData(api_url)
      

# Save data into file
with open('data_coment_tiki.json', 'w', encoding='utf-8') as file:
 json.dump(comment_list, file)