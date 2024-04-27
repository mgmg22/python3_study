from bs4 import BeautifulSoup, Tag
import requests
import notify

xb_list = []


def filter_list(tr):
    title = tr.get_text()
    href = 'http://www.0818tuan.com' + tr['href']
    blackList = [
        "【顶】",
        "定位", "部分", "山东", "福建", "江苏", "云南", "江西", "河北", "广州", "广东",
        "首单", "盲盒", "需要邀请", "前10", "点秒杀", "点试用", "月黑风高", "生日礼", "多拍",
        "件", "限量", "如有", "折合", "到手", "进口", "买家", "小法庭",
        "求", "啥", "咋", "呢", "请问", "请教", "怎么", "怎样", "咨询", "居然要", "都多少",
        "黄了", "没了", "果熟", "有果", "油果", "18cm",
        "茅台", "京造", "东方甄选", "京东买药",
        "洗衣液", "內衣", "火锅",
        "联通", "流量", "单车", "客服", "风险", "美元", "迅雷",
        "邮储联名",
    ]
    if any(sub in title for sub in blackList):
        return False
    whiteList = [
        "云闪付", "ysf",
        "xyk", "性用卡", "还款",
        "中国银行", "中行", "农业银行", "农行", "交通银行", "交行", "浦发", "邮储", "光大", "平安",
        "工商银行", "工行", "工银", "e生活",
        "建设银行", "建行", "建融", "善融",
        "招商银行", "招行", "掌上生活", "体验金",
        "中信", "动卡空间",
        "微众",
        "淘宝", "tb", "手淘", "猫超", "闲鱼", "高德",
        "支付宝", "zfb", "转账", "网商",
        "微信", "wx", "vx", "v.x", "V.x", "小程序", "立减金",
        "京东", "狗东", "JD", "京豆", "e卡",
        "抖音", "dy",
        "美团", "饿了么", "elm",
        "红包", "抽奖", "秒到", "保底", "游戏", "下载",
        # "同程", "携程", "途牛",
        "话费", "移动", "和包", "电信", "Q币", "扣币",
        "麦当劳", "肯德基", "必胜客", "星巴克", "瑞幸", "朴朴", "喜茶", "霸王茶姬", "百果园", "茶百道",
        "礼品卡", "星礼卡", "苹果卡",
        "深圳通",
    ]
    if any(sub in title for sub in whiteList):
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


def get_content(href):
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
