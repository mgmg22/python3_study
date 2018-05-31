data = {
    'appid': 'wxd930ea5d5a258f4f',
    'mch_id': 10000100,
    'device_info': 1000,
    'body': 'test',
    'nonce_str': 'ibuaiVcKdpRxkhJA',
    'test': None
}


def parse_to_xml(data):
    xml = '<Xml>'
    for key in data.keys():
        xml += "<{0}>{1}</{0}>\n".format(key, data.get(key))
    xml += '</Xml>'
    return xml


def get_sign(data):
    check = []
    for key in data.keys():
        if data.get(key) is None:
            check.append(key)
    for key in check:
        data.pop(key)
    sign = "&".join(sorted("{0}={1}".format(key, data.get(key)) for key in data.keys()))
    sign += "&key=192006250b4c09247ec02edce69f6a2d"
    return md5(sign)


def md5(str):
    return str


data['sign'] = get_sign(data)
print(parse_to_xml(data))
