# coding:utf-8
import wx_pay_util


def get_response():
    data = {
        'appid': "wxdace645e0bc2c424",
        'mch_id': '1900008951',
        'nonce_str': 'ibuaiVcKdpRxkhJA',
        'sub_mch_id': '218224494',
        'out_trade_no': '2018060515533101817182221344',
    }
    url = "pay/orderquery"
    secret = '3AC991426F056322E053645AA8C0CC12'
    wechat = wx_pay_util.WechatDroid(url, data, secret)
    wechat.save()


if __name__ == '__main__':
    get_response()
