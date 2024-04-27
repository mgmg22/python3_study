from bs4 import BeautifulSoup, Tag
import requests
import notify

xb_list = []


def filter_list(tr):
    title = tr.get_text()
    href = 'http://www.0818tuan.com' + tr['href']
    ignoreConditions = [
        "【顶】" in title,
        "定位" in title,
        "首单" in title,
        "山东" in title,
        "福建" in title,
        "江苏" in title,
        "云南" in title,
        "江西" in title,
        "部分地区" in title,
        "洗衣液" in title,
        "盲盒" in title,
        "到手" in title,
        "咨询" in title,
    ]
    if any(ignoreConditions):
        return False
    substrings = [
        "转账",
        "招行",
        "工行",
        "建行",
        "中行",
        "zfb",
        "支付宝",
        "京东",
        "京豆",
        "手淘",
        "淘宝",
        "微信",
        "vx",
        "wx",
        "抖音",
        "dy",
        "xyk",
        "还款",
        "红包",
        "猫超",
        "瑞幸",
        "朴朴",
        "同程",
        "携程",
    ]
    if any(sub in title for sub in substrings):
        print(title)
        print(href)
    else:
        return False
    item = {
        'title': title,
        'href': href,
        'content': get_content(href)
    }
    xb_list.append(item)


def get_content(href) -> Tag:
    data = requests.get(href)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    xb_content = soup.select('div.genxin')
    if not xb_content:
        xb_content = soup.select('#xbcontent > p')
    # print(xbcontent[0])
    return xb_content[0]


def get_top_summary():
    url = 'http://www.0818tuan.com/list-1-0.html'
    data = requests.get(url)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    tr_elements = soup.select('#redtag>.list-group-item')
    for tr in tr_elements:
        filter_list(tr)


def notify_markdown():
    content = ''
    for item in xb_list:
        content += f'''
##### [{item['title']}]({item['href']})
{item['content']}
'''
    notify.pushplus_bot_my(xb_list[0]["title"], content)
    with open("xb.md", 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    get_top_summary()
    notify_markdown()
