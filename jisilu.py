# coding:utf-8
# 爬取集思录帖子
from bs4 import BeautifulSoup
import requests

url = 'https://www.jisilu.cn/explore/'
headers = {}

data = requests.get(url, headers=headers)
data.encoding = 'utf-8'
# print(data.status_code)
# print(data.encoding)
soup = BeautifulSoup(data.text, 'lxml')
links = soup.select('div.aw-questoin-content > h4 > a:nth-of-type(1)')
# print(links)
for index, item in enumerate(links):
    print(index, item.get_text(), item.get('href'))
