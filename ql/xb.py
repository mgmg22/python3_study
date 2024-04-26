from bs4 import BeautifulSoup
import requests
import notify

xb_list = []


# 定义一个过滤函数，用于移除包含特定字符串的tr元素
def filter_list(tr):
    title = tr.get_text()
    href = tr['href']
    ignoreConditions = [
        "【顶】" in title,
    ]
    if any(ignoreConditions):
        return False
    substrings = ["zfb",
                  "转账",
                  "招行",
                  "工行",
                  "建行",
                  "中行",
                  "支付宝",
                  "微信",
                  "京东",
                  "vx",
                  "xyk",
                  "还款",
                  "红包",
                  "猫超",
                  ]
    # 使用all()函数和not in操作符判断my_string是否不包含substrings中的任意一个字符串
    if any(sub in title for sub in substrings):
        print(title)
    else:
        return False
    item = {
        'title': title,
        'href': href
    }
    xb_list.append(item)


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
[{item['title']}](http://www.0818tuan.com/{item['href']})
'''
    notify.pushplus_bot_my(xb_list[0]["title"], content)
    with open("xb.md", 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    get_top_summary()
    notify_markdown()
