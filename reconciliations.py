#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : reconciliations.py
# @Author: sxs
# @Date  : 2018/6/28
# @Desc  :
import copy
import csv
import hashlib


class Order(object):
    bill_date = None
    order_sn = None
    order_wx = None
    pay_type = None
    state = None
    fee = None
    amount = None
    refund = None
    fee_rate = None

    def __init__(self, order_sn, state, amount, fee_rate, *karges):
        self.order_sn, self.state, self.amount, self.fee_rate = order_sn, state, amount, fee_rate

    def __hash__(self):
        return hash(md5(self.order_sn + self.state + self.amount + self.fee_rate))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __str__(self):
        return '商户订单号={}交易类型={}总金额={}费率={}'.format(self.order_sn, self.state, self.amount, self.fee_rate)


def format_order(str):
    return str.replace('`', '')


def md5(before_str):
    """
    获取md5
    :param before_str:
    :return:
    """
    return hashlib.md5(before_str.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    a = set()
    b = set()
    with open('test.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if index == 0:
                continue
            order = Order(format_order(row[6]), row[9], row[12], row[23])
            order.channel = '0'
            sub_order = copy.deepcopy(order)
            sub_order.channel = '1'
            a.add(order)
            b.add(sub_order)
            print(order == sub_order)
    print(a)
    for item in a:
        print(item)
