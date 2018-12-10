#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : http_unit.py
# @Author: sxs
# @Date  : 2018/8/8
# @Desc  : 网络请求单元测试
import hashlib
import json

import requests


def md5(before_str):
    """
    获取md5
    :param before_str:
    :return:
    """
    return hashlib.md5(before_str.encode('utf-8')).hexdigest()


head = {
    "access-token": '817ed196dcf669dc4fddf6de618bb753'
}

youdian_head = {
    "Charset": 'UTF-8',
    "clientSort": 'android',
    "version": '5.0.1.0-8'
}
# 生成验签的key
key = '0226dee8829c64a16c53a3029f8ddb69'


def unit_get():
    ur30 = "https://merchantapp-admin-test.51fubei.com/appv2/public/gaode-regeo?location=120.069739,30.329171&key=8ab9d87355013e07bfcf7e9423b87e75&" \
           "sign=f8b3a9c4661b8ebb399b4b7d00aeba69"
    data = requests.get(ur30, headers=head)
    print(data.text)
    Token = head.get('access-token')
    str = '{"location":"120.069739,30.329171","key":"8ab9d87355013e07bfcf7e9423b87e75"}' + Token + key
    print(md5(str))


# fubei 接口
def unit_post():
    url = 'https://merchantapp-admin-test.51fubei.com/app/public/upload-image'
    token = head.get('access-token')
    before_str = '{"image":"/9j/4AAQSkZJRgABAQAAAQAZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAAdACMDAEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NT6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8BAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSdYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqwsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAKKAP6W/wDiFZ/4KJf9Fn/Y2/8ADifHb/6Gij/iFZ/4Ev+IVn/AIKJf9Fn/Y2/8OJ8dv8A6Gij/iFZ/wCCiX/RZ/2Nv/DifHb/AOhor++KJf9Fn/Y2/8ADifHb/6Giiv"}'
    req_body = json.loads(before_str)
    req_body['sign'] = md5(before_str + token + key)
    print(req_body)
    data = requests.post(url, headers=head, data=req_body)
    print(data.text)


# 友店商户版接口测试
def test_youdian():
    url = 'http://youdian-app-test.51youdian.com:8081/saledianMerchant/LifeCircle/User/login'
    before_str = '{"platform":"1", "password":"6846860684f05029abccc09a53cd66f1", "sign":"e812182fef64438ecee33d66c4bffaee", "apb_nonce":"e4b362e2e51c40e38d77c1c142b54421", "username":"多通道1", "registrationId":"140fe1da9e9a212147f"}'
    req_body = json.loads(before_str)
    data = requests.post(url, headers=youdian_head, data=req_body)
    print(data.text)


# crm接口测试
def test_crm():
    url = 'http://172.16.21.240:8086/gateway'
    content = {
        "mobile": "15757179463",
        "userId": "123"
    }
    crm_body = {
        "appid": "123",
        "method": "fshows.market.api.openaccount.merchant.precreate",
        "token": "123",
        "sign": "456",
        "version": "1.0",
        "appinfo": {},
        "content": json.dumps(content)
    }
    data = requests.post(url, data=crm_body)
    print(data.text)


if __name__ == '__main__':
    # unit_post()
    # test_youdian()
    test_crm()
