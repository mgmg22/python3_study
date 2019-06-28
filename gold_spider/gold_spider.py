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
CMB_url = 'https://ai.cmbchina.com/MBWebService/AjaxMetModuleInfo.ashx?pageID=C8455BD9-8AD4-4B56-A193-22142C9EB3C1&moduleID=AC730DC5-8F5F-46BE-9DB4-9273E26205EC&ModuleName=MetPrc&randnum=0.5888150773659064'

ding_url = "https://oapi.dingtalk.com/robot/send?access_token=aee7d29cb485f16a3e9c9546aed3f466fbe7743f1d630bc78636c732e7fcec58"
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


# 国美黄金价格
def get_gm():
    result = session.post(GM_url)
    data = json.loads(result.text)
    print(data['responseParams'])
    gold['国美'] = data['responseParams']


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
    gold['招行'] = "{}\t买: {}\t {}".format(
        data['Msg'][0]['MetPrc'],
        data['Msg'][1]['MetPrc'],
        data['Msg'][2]['PrcCvt'] + data['Msg'][2]['MetPrc'] + "%")
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
    get_gm()
    get_ICBC()
    get_cmb()
    send_ding()
