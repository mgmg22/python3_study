import hashlib

from bs4 import BeautifulSoup


class WechatDroid:
    def __init__(self, data, secret):
        self.data = data
        self.secret = secret
        self.get_sign()

    # 列表转xml
    def parse_to_xml(self):
        xml = '<xml>'
        for key in self.data.keys():
            xml += "<{0}><![CDATA[{1}]]></{0}>\n".format(key, self.data.get(key))
        xml += '</xml>'
        return xml

    # 获取sign
    def get_sign(self):
        check = []
        for key in self.data.keys():
            if self.data.get(key) is None:
                check.append(key)
        for key in check:
            self.data.pop(key)
        sign = "&".join(sorted("{0}={1}".format(key, self.data.get(key)) for key in self.data.keys()))
        sign += "&key=" + self.secret
        self.data['sign'] = md5(sign)

    def trans_xml_to_dict(self):
        """
        将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象

        :param xml: 原始 XML 格式数据
        :return: dict 对象
        """
        soup = BeautifulSoup(self.parse_to_xml(), features='xml')
        xml = soup.find('xml')
        if not xml:
            return {}
        # 将 XML 数据转化为 Dict
        data = dict([(item.name, item.text) for item in xml.find_all()])
        return data


# 获取md5
def md5(before_str):
    return str(hashlib.md5(before_str.encode()).hexdigest()).upper()
