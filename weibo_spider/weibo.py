#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : weibo.py
# @Author: sxs
# @Date  : 2018/7/21
# @Desc  :微博数据-词云
import codecs
import csv
import os
import re

import jieba.analyse
import matplotlib.pyplot as plt
import requests
from wordcloud import WordCloud

# api = 'https://m.weibo.cn/api/container/getIndex?pids[]=Pl_Official_MyProfileFeed__20&pids[]=Pl_Official_MyProfileFeed__20&profile_ftype[]=1&profile_ftype[]=1&is_all[]=1&is_all[]=1&jumpfrom=weibocom&sudaref=login.sina.com.cn&type=uid&value=2843500544&containerid=1076032843500544&page=%s'
api = 'https://m.weibo.cn/api/container/getIndex?uid=5088151536&luicode=10000011&lfid=1076035088151536&type=uid&value=5088151536&containerid=1076035088151536&page=%s'
csv_path = 'weibo.csv'


def fetch_weibo():
    for i in range(1, 100):
        response = requests.get(url=api % i)
        # 没有该页数据跳出循环
        if response.json().get('ok') == 0:
            break
        cards = response.json().get('data').get('cards') or []
        for group in cards:
            # print(group)
            if group.get("mblog"):
                text = group.get("mblog").get("text")
                text = text.encode("utf-8")
                text = cleanring(text).strip()
                if text:
                    yield text


def cleanring(temp):
    temp = temp.decode("utf8")
    # 去除标点
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", temp)
    # 去除html
    dr = re.compile(r'<[^{}]+>', re.S)
    dd = dr.sub('', string)
    return dd.replace('分享图片​​​', '').replace('转发微博', '')


def write_csv(texts):
    with codecs.open(csv_path, 'w', 'utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["text"])
        writer.writeheader()
        for text in texts:
            writer.writerow({"text": text})


def read_csv():
    with codecs.open(csv_path, 'r', 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['text']


# 分词处理
def word_segment(texts):
    jieba.analyse.set_stop_words("stopwords.txt")
    for text in texts:
        tags = jieba.analyse.extract_tags(text, topK=20)
        yield " ".join(tags)


# 生成图片
def generate_img(texts):
    data = " ".join(text for text in texts)
    mask_img = plt.imread('./heart-mask.jpg')
    wordcloud = WordCloud(
        scale=2,
        font_path='msyh.ttc',
        background_color='white',
        mask=mask_img
    ).generate(data)
    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud.to_file('./wordcloud.jpg')


if __name__ == '__main__':
    if os.path.exists(csv_path):
        pass
    else:
        write_csv(fetch_weibo())
    word = word_segment(read_csv())
    generate_img(word)
