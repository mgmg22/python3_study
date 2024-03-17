#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stock_spider.py
# @Author: sxs
# @Date  : 2024/03/17
# @Desc  : jsl指数涨幅统计,生成markdown表格

import notify
import requests

filters = {
    '上证指数',
    '上证50',
    '科创50',
    '创业板指',
    '沪深300',
    '北证50',
}


# 指数涨幅统计
def get_stock_index() -> list:
    list_url = 'https://www.jisilu.cn/data/idx_performance/list/?___jsl=LST___t=1710685332681'
    resp = requests.post(list_url)
    data = []
    for row in resp.json()['rows']:
        if row['cell']['index_nm'] in filters:
            stock = {'name': row['cell']['index_nm'],
                     'increase': row['cell']['increase_rt'],
                     }
            data.append(stock)
    return data


def notify_markdown(stocks: list):
    content = '''# 指数涨幅统计
| 名称 | 本日涨幅 |
|:--------|--------:|
'''
    for item in stocks:
        content += f'| {item["name"]} | {item["increase"]} |\n'

    title = "今日" + stocks[0]["name"] + "涨幅为:" + stocks[0]["increase"]
    notify.serverJMy(title, content)


if __name__ == '__main__':
    stock = get_stock_index()
    notify_markdown(stock)
