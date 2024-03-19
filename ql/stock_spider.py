#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : stock_spider.py
# @Author: sxs
# @Date  : 2024/03/17
# @Desc  : jsl指数涨幅统计,生成markdown表格

import notify
import requests

indexFilters = {
    '上证指数',
    '上证50',
    '科创50',
    '创业板指',
    '沪深300',
    '北证50',
}

# TODO
etf_url = 'https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___t=1710853843396&rp=25&page=1'
ETFFilters = {
    # 512690	酒ETF
    # 512760	芯片ETF
    '酒ETF',
    '芯片ETF',
}

notifyData = []


# 指数涨幅统计
def get_stock_index():
    list_url = 'https://www.jisilu.cn/data/idx_performance/list/?___jsl=LST___t=1710685332681'
    resp = requests.post(list_url)
    for row in resp.json()['rows']:
        if row['cell']['index_nm'] in indexFilters:
            stock = {'name': row['cell']['index_nm'],
                     'increase': row['cell']['increase_rt'],
                     }
            notifyData.append(stock)


#  专门获取医药生物（801150.SL）的数据
def add_SW_increase():
    sw_url = 'https://www.swsresearch.com/institute-sw/api/index_publish/details/index_spread/?swindexcode=801150'
    headers = {
        'accept': "*/*",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    resp = requests.get(sw_url, headers=headers)
    data = resp.json()['data'][0]
    lastDay = float(data['l3'])
    now = float(data['l8'])
    swData = {'name': "医药生物",
              'increase': str(round(((now - lastDay) / lastDay) * 100, 2)),
              }
    notifyData.append(swData)


def notify_with_markdown():
    content = '''# 指数涨幅统计
| 名称 | 本日涨幅 |
|:--------|--------:|
'''
    for item in notifyData:
        content += f'| {item["name"]} | {item["increase"]} %|\n'
    notify.serverJMy(generate_title(), content)
    # with open("Test.md", 'w') as f:
    #     f.write(content)


def generate_title() -> str:
    return "今日" + notifyData[0]["name"] + "涨幅为:" + notifyData[0]["increase"] + "%"


if __name__ == '__main__':
    get_stock_index()
    add_SW_increase()
    notify_with_markdown()
