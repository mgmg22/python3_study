#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : http_unit.py
# @Author: sxs
# @Date  : 2020/1/18
# @Desc  : 读取项目中的Activity的名称,需要安装lxml库
from bs4 import BeautifulSoup

if __name__ == '__main__':
    file = open("./AndroidManifest.xml", encoding='utf-8').read()
    soup = BeautifulSoup(file, features='xml')
    print(f"共有{len(soup.application.find_all('activity'))}个Activity")
    for item in soup.application.find_all('activity'):
        print(item.get("android:name"), item.get("android:label"))
