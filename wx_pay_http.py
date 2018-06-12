# coding:utf-8
from wx_pay_util import parse_to_xml, get_sign, trans_xml_to_dict
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
    request_data = get_sign(data, secret)
    # print(parse_to_xml(request_data))
    response = requests.post(url, data=parse_to_xml(request_data))
    # print(bytes.decode(response.content))
    print(trans_xml_to_dict(parse_to_xml(request_data)))
    with open('out.txt', "wb") as out:
        out.write(response.content)


if __name__ == '__main__':
    get_response()
