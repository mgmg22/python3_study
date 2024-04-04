#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stock_spider.py
# @Author: sxs
# @Date  : 2024/04/04
# @Desc  : 微博热搜列表
from bs4 import BeautifulSoup
import requests

verify = False

summary = []


# 定义一个过滤函数，用于移除包含特定字符串的tr元素
def filter_tr(tr):
    print("-----")
    # 序号、置顶
    td_text1 = tr.select('td.td-01')
    # 超链接 数量
    td_text2 = tr.select('td.td-02')
    # icon 新、热、暖
    td_text3 = tr.select('td.td-03')
    text = td_text2[0].find('a').get_text()
    num = td_text1[0].get_text()
    # td_text = tr.find('td').get_text()
    # print(str(td_text1[0]))
    # print(num+text)
    # print(text)
    print(td_text3[0])
    # 过滤置顶
    if "icon-top" in str(td_text1[0]):
        return False
    if "剧集" in str(td_text2[0]):
        return False
    # todo 过滤广告
    return num + "." + text


def get_top_summary():
    url = 'https://s.weibo.com/top/summary'
    # todo 环境变量
    headers = {
        'Cookie': "SUB=_2AkMRUtBSf8NxqwFRmfsUxGrkbop-wg7EieKnDiGJJRMxHRl-yT9kql1ZtRB6OtL-vTbTNhcLy7AgHY2b5GT7UADcvUnR; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5B4Q3QrW71r.NcWldvRS-8; _s_tentry=passport.weibo.com; Apache=4426240446675.045.1712217957934;",
    }
    data = requests.get(url, headers=headers, verify=verify)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    tr_elements = soup.select('#pl_top_realtimehot > table > tbody> tr')

    filtered_values = [filter_tr(tr) for tr in tr_elements if filter_tr(tr)]

    # todo notify
    print(filtered_values)


if __name__ == '__main__':
    get_top_summary()
    # todo notify
