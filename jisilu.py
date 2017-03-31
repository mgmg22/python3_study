# coding:utf-8
# 爬取集思录帖子
from bs4 import BeautifulSoup
import requests

url = 'https://www.jisilu.cn/explore/'
headers = {}


def read_main():
    data = requests.get(url, headers=headers)
    data.encoding = 'utf-8'
    # print(data.status_code)
    # print(data.encoding)
    soup = BeautifulSoup(data.text, 'lxml')
    links = soup.select('div.aw-questoin-content > h4 > a:nth-of-type(1)')
    # print(links)
    with open('./jsl_text.txt', 'w') as f:
        for index, item in enumerate(links):
            print(index + 1, '#', item.get_text(), item.get('href'))
            f.write(str(index + 1) + '#' + item.get_text() + ' ' + item.get('href') + '\n')

            def read_detail(item_url):
                data_item = requests.get(item_url)
                data_item.encoding = 'utf-8'
                soup_item = BeautifulSoup(data_item.text, 'lxml')
                try:
                    info = soup_item.select('div.aw-mod-body > div.aw-question-detail-txt ')
                    dates = soup_item.select('div.aw-question-detail-meta > span')
                    print(dates[0].get_text(), '||', info[0].get_text().strip().replace('\n', ' '))
                    f.write(dates[0].get_text() + '||' + info[0].get_text().strip() + '\n')
                except:
                    pass

            read_detail(item.get('href'))  # 打印帖子内容


if __name__ == '__main__':
    read_main()
