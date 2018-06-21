import hashlib

import requests

from xml_util import dict_to_xml, xml_to_dict


class WechatDroid(object):
    base_url = 'https://api.mch.weixin.qq.com/'

    def __init__(self, url, data, secret):
        self.session = requests.session()
        self.url = self.base_url + url
        self.secret = secret
        self.data = self.get_sign(data)

    def get_sign(self, data):
        """
        获取sign
        :return:
        """
        check = []
        for key in data.keys():
            if data.get(key) is None:
                check.append(key)
        for key in check:
            data.pop(key)
        sign = "&".join(sorted("{}={}".format(key, data.get(key)) for key in data.keys()))
        sign += "&key={}".format(self.secret)
        data['sign'] = md5(sign)
        return data

    def post(self):
        response = self.session.post(self.url, data=dict_to_xml(self.data))
        return response

    def save(self):
        response = self.post()
        print(xml_to_dict(bytes.decode(response.content)))
        with open('WX.csv', "w") as out:
            out.write(bytes.decode(response.content))


def md5(before_str):
    """
    获取md5
    :param before_str:
    :return:
    """
    return hashlib.md5(before_str.encode('utf-8')).hexdigest().upper()
