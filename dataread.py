# coding:utf-8
# 获取帖子内容
from bs4 import BeautifulSoup
import requests


def readDetail(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'lxml')
    try:
        info = soup.select('div.aw-mod-body > div.aw-question-detail-txt ')
        dates = soup.select('div.aw-question-detail-meta > span')
        print(dates[0].get_text(), info[0].get_text().strip().replace('\n', ' ') + '\n')
    except:
        pass
