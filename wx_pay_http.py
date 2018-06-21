# coding:utf-8
import wx_pay_util
import requests

data = {
    'appid': "wxdace645e0bc2c424",
    'mch_id': '1900008951',
    'nonce_str': 'ibuaiVcKdpRxkhJA',
    'sub_mch_id': '218224494',
    'out_trade_no': '2018060515533101817182221344',
}
secret = '3AC991426F056322E053645AA8C0CC12'

url = "https://api.mch.weixin.qq.com/pay/orderquery"


def get_response():
    wechat = wx_pay_util.WechatDroid(data, secret)
    # print(wechat.parse_to_xml())
    response = requests.post(url, data=wechat.parse_to_xml())
    # print(bytes.decode(response.content))
    print(wechat.trans_xml_to_dict())
    with open('WX.txt', "wb") as out:
        out.write(response.content)


if __name__ == '__main__':
    get_response()
