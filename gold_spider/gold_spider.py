#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : gold_spider.py
# @Author: sxs
# @Date  : 2018/11/29
# @Desc  : 爬黄金价格

import json

import requests

ICBC_url = 'https://mybank.icbc.com.cn/servlet/AsynGetDataServlet'
CMB_url = 'https://ai.cmbchina.com/MBWebService/AjaxMetModuleInfo.ashx?pageID=C8455BD9-8AD4-4B56-A193-22142C9EB3C1&moduleID=AC730DC5-8F5F-46BE-9DB4-9273E26205EC&ModuleName=MetPrc&randnum=0.5888150773659064'

ding_url = "https://oapi.dingtalk.com/robot/send?access_token=d91863f33abc66ac08b0381f544fa2f4df1905814ba75617eb668d06d61655bd"
ding_header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}
gold = {}
session = requests.session()
icbc = {
    "Area_code": "0200",
    "trademode": 1,
    "proIdsIn": "",
    "isFirstTime": 1,
    "tranCode": "A00462"
}


# 工行黄金价格
def get_ICBC():
    result = session.post(ICBC_url, data=icbc)
    data = json.loads(result.text)
    # print(data)
    gold['工行'] = "{}\t买: {}\t {}\t{}".format(
        data['market'][0]['buyprice'],
        data['market'][0]['sellprice'],
        data['market'][0]['openprice_dr'],
        data['market'][0]['openprice_dv'])
    print(gold['工行'])


# 招行黄金价格
def get_cmb():
    result = session.get(CMB_url)
    data = json.loads(result.text)
    gold['招行'] = "{}\t {}".format(
        data['scrollpgoldmsg'][0]['latestPrice'],
        data['scrollpgoldmsg'][0]['upDownRange'] + "%")
    print(gold['招行'])


# 通知钉钉机器人
def send_ding():
    result = ""
    for key in gold:
        result += str(key) + "\t" + str(gold[key]) + "\n"
    data = {
        "msgtype": "text",
        "text": {
            "content": result
        }
    }
    ding_data = json.dumps(data)
    requests.post(ding_url, data=ding_data, headers=ding_header)


if __name__ == '__main__':
    get_ICBC()
    get_cmb()
    send_ding()
