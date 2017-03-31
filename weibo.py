import codecs
import csv
import re

import jieba.analyse
import matplotlib.pyplot as plt
import requests
# from scipy.misc import imread
from wordcloud import WordCloud

cookies = {
    "_T_WM": "2e88164fbbfc454e4cf86c45b4bea59c",
    "M_WEIBOCN_PARAMS": "lfid%3D1001018008633021200000000%26luicode%3D10000370.",
    "SUHB": "0XDlotSWxjgopb",
    "SUB": "_2A2511kV7DeRxGeNM7lcY8i3NwzSIHXVXOWszrDV6PUJbkdBeLVemkW2e6G09R7CSMfzS4JfMgjSuG2-6Qg..",
    "SCF": "AgWZEtv_r35-cHl2D_TuV25cmnk-fsIM1v9NuuVwIY2hdCrYhRjGZ8GUXFT4SDGscxnUI-eUQACiAHzurw-kf3o."
    # "ALF": "xxxx",
    # "SCF": "xxxxxx.",
    # "SUBP": "xxxxx",
    # "SUB": "xxxx",
    # "SUHB": "xxx-", "xx": "xx", "_T_WM": "xxx",
    # "gsScrollPos": "", "H5_INDEX": "0_my", "H5_INDEX_TITLE": "xxx",
    # "M_WEIBOCN_PARAMS": "xxxx"
}


# def fetch_weibo():
api = "http://m.weibo.cn/index/my?format=cards&page=%s"
for i in range(2, 3):
    response = requests.get(url=api % i, cookies=cookies)
    print(response.json()[0])
    data = response.json()[0]
    groups = data.get("card_group") or []
    for group in groups:
        text = group.get("mblog").get("text")
        text = text.encode("utf-8")
        def cleanring(content):
            """
            去掉无用字符
            """
            pattern = "<a .*?/a>|<i .*?/i>|//@：转发微博|转发微博|//:|Repost|，|？|。|、|分享图片"
            print(content)
            # content = content.decode('utf-8')
            # print(content)
            content = re.sub(pattern, "", content)
            print(content)
            return content
        text = cleanring(text).strip()
        # yield text


# if __name__ == '__main__':
#     texts = fetch_weibo()
#     print(texts)
    # write_csv(texts)
    # generate_img(word_segment(read_csv()))
