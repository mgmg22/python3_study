#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stock_spider.py
# @Author: sxs
# @Date  : 2024/03/17
# @Desc  : jsl个股详情
from bs4 import BeautifulSoup
import requests


def get_stock_detail(stock):
    url = 'https://www.jisilu.cn/data/stock/' + stock
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'lxml')
    price = soup.select('#stock_detail > tr:nth-child(1) > td:nth-child(2)> span > a')
    increase = soup.select('#stock_detail > tr:nth-child(1) > td:nth-child(3)> span')
    name = soup.select('div.grid-row>table>tr>td>div>a')
    print(name[0].text + price[0].text)
    swData = {
        'id': stock,
        'name': name[0].text,
        'price': price[0].text,
        'increase': increase[0].text
    }
    return swData
