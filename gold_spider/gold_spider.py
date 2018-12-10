#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : gold_spider.py
# @Author: sxs
# @Date  : 2018/11/29
# @Desc  : 爬黄金价格

import requests
import json

GM_url = 'https://www.gomegold.com/Index/MethodQuoteprice'
ICBC_url = 'https://mybank.icbc.com.cn/servlet/AsynGetDataServlet'

ding_url = "https://oapi.dingtalk.com/robot/send?access_token=aee7d29cb485f16a3e9c9546aed3f466fbe7743f1d630bc78636c732e7fcec58"
ding_header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}
low = 267
high = 275
gold = {}
session = requests.session()
icbc = {
    "Area_code": "0200",
    "trademode": 1,
    "proIdsIn": "",
    "isFirstTime": 1,
    "tranCode": "A00462"
}


# 国美黄金价格
def get_gm():
    result = session.post(GM_url)
    data = json.loads(result.text)
    print(data['responseParams'])
    gold['国美黄金'] = data['responseParams']


# 工行黄金价格
def get_ICBC():
    result = session.post(ICBC_url, data=icbc)
    data = json.loads(result.text)
    print(data['market'][0]['buyprice'])
    gold['工商银行'] = data['market'][0]['buyprice']


# 通知钉钉机器人
def send_ding():
    data = {
        "msgtype": "text",
        "text": {
            "content": gold
        }
    }
    ding_data = json.dumps(data)
    requests.post(ding_url, data=ding_data, headers=ding_header)


def check_price(price):
    global high, low
    high = max(price, high)
    low = low(price, low)


if __name__ == '__main__':
    get_gm()
    get_ICBC()
    send_ding()
