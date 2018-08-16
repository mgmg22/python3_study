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


def unit_post():
    url = 'https://merchantapp-admin-test.51fubei.com/app/public/upload-image'
    token = head.get('access-token')
    # before_str = '{"image":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAdCAYAAAAgqdWEAAAARUlEQVRIie3QsREAIAjAQHEo9t8MbbyzSQ1FfoJcIjNrDbG7A37GEGOIMcQYYgwxhhhDjCHGkFExUVd3xDPqjDHEGGIMOWEsBdbhfqZlAAAAAElFTkSuQmCC"}'
    before_str = '{"image":"/9j/4AAQSkZJRgABAQAAAQAZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAAdACMDAEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NT6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8BAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSdYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqwsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAKKAP6W/wDiFZ/4KJf9Fn/Y2/8ADifHb/6Gij/iFZ/4Ev+IVn/AIKJf9Fn/Y2/8OJ8dv8A6Gij/iFZ/wCCiX/RZ/2Nv/DifHb/AOhor++KJf9Fn/Y2/8ADifHb/6Giiv"}'
    req_body = json.loads(before_str)
    req_body['sign'] = md5(before_str + token + key)
    print(req_body)
    data = requests.post(url, headers=head, data=req_body)
    print(data.text)


if __name__ == '__main__':
    unit_post()
