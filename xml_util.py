#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : xml_util.py
# @Author: sxs
# @Date  : 2018/6/21
# @Desc  : \
from bs4 import BeautifulSoup


def dict_to_xml(data):
    """
    列表转xml
    :param data:
    :return:
    """
    xml = '<xml>'
    for key in data.keys():
        xml += "<{0}><![CDATA[{1}]]></{0}>\n".format(key, data.get(key))
    xml += '</xml>'
    return xml


def xml_to_dict(data):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象

    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """
    soup = BeautifulSoup(data, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
    return data
