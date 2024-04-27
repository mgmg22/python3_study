from bs4 import BeautifulSoup, Tag
import requests
import notify

xb_list = []


def filter_list(tr):
    title = tr.get_text()
    href = 'http://www.0818tuan.com' + tr['href']
    ignoreStrings = [
        "【顶】",
        "定位",
        "首单", "盲盒",
        "部分地区", "山东", "福建", "江苏", "云南", "江西", "河北", "广州",
        "到手",
        "买家",
        "茅台", "洗衣液", "內衣",
        "流量", "单车",
        "请问", "请教", "有啥", "怎么", "黄了", "咨询",
    ]

    if any(sub in title for sub in ignoreStrings):
        return False
    substrings = [
        "招商银行", "招行", "掌上生活",
        "工商银行", "工行", "工银", "e生活",
        "建设银行", "建行", "建融",
        "中国银行", "中行", "农业银行", "农行", "交通银行", "交行", "浦发", "邮储", "光大", "平安",
        "中信", "动卡空间",
        "微众",
        "云闪付", "ysf",
        "xyk", "性用卡", "还款",
        "淘宝", "tb", "手淘", "猫超", "闲鱼",
        "支付宝", "zfb", "转账", "网商",
        "微信", "vx", "wx", "小程序", "立减金",
        "京东", "京豆", "e卡",
        "抖音", "dy",
        "美团", "饿了么", "elm",
        "红包",
        "同程", "携程", "途牛",
        "话费", "移动", "和包", "电信",
        "麦当劳", "肯德基", "必胜客", "星巴克", "瑞幸", "朴朴", "喜茶", "霸王茶姬", "百果园", "茶百道",
        "礼品卡", "星礼卡", "苹果卡",
        "深圳通",
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
    # todo content条件过滤
    xb_list.append(item)


def get_content(href) -> str | Tag:
    data = requests.get(href)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    xb_content = soup.select('div.genxin')
    if not xb_content:
        xb_content = soup.select('#xbcontent > p')
    if not xb_content:
        print("获取帖子内容异常")
        return ''
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
