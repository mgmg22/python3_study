from bs4 import BeautifulSoup
import requests
import notify

xb_list = []


def filter_list(tr):
    title = tr.get_text()
    href = 'http://www.0818tuan.com' + tr['href']
    commonBlackList = [
        "定位", "部分", "东北", "徽", "北京", "天津", "重庆",
        "山东", "福建", "江苏", "云南", "江西", "河北", "广东", "吉林", "湖北", "河南", "陕西", "湖南", "四川", "宁夏",
        "广西", "辽宁",
        "厦门", "南京", "东莞", "广州", "南海", "苏州", "中山", "常州", "青岛", "成都", "武汉", "合肥",
        # ----卡----
        "平安X", "平安x", "中行x", "民生x", "邮储x", "农行x", "交行x", "光大x", "阳光惠生活", "平安银行X", "平安银行信",
        "邮储联名", "邮储美团联名", "闪光卡", "广发", "恒丰", "浦大喜奔", "缤纷生活", "万事达", "汇丰", "农商",
        "宝石山", "众邦", "联名卡",
    ]
    highBlackList = [
        "【顶】",
        # ----玩法----
        "需要邀请", "特邀", "受邀", "助力",
        "首单", "盲盒", "月黑风高", "和包生日", "生日礼", "生日分享", "生日红包", "互换", "入会", "买1送1", "买一送一",
        # ----网购----
        "件", "/袋", "/盒", "箱", "罐",
        "限量", "如有", "折合", "到手", "进口", "买家", "小法庭", "单号", "预售", "客服",
        "健康", "亚瑟", "查询", "高佣", "想买",
        # "瓶",
        # "返",
        # "凑",
        # ----语气----
        "问题", "问问", "问下", "谢谢", "请问", "问一下", "什么", "请教", "求", "咋", "怎么", "怎样", "咨询", "赐教",
        "有没有", "有问",
        "啥", "呢", "居然要", "都多少", "是多少", "是不是", "便宜啊", "麻烦", "帮忙看", "能不能", "哪来的", "卧槽",
        "牛逼", "还好",
        "吗？", "吧？", "了？", "了?", "链接？", "么？", "呀!", "啊？", "啦 ！", "了啊",

        # ----负面----
        "黄了", "没了", "果熟", "有果", "油果", "续费", "拦截", "删了", "不玩了", "黑号", "号黑", "限制使用",
        "被盗", "崩溃", "差评", "长期出", "监控", "套牢", "猫饼", "怀疑", "未到账", "过期", "领完了", "凉了", "凉凉",
        "不能卖", "垃圾", "逾期", "风控", "收腰",
        # ----虚拟----
        "风险", "美元", "提额", "保险", "开通", "境外",
        "迅雷", "唯品会小程序", "爱奇艺红包", "电子书", "贷",
        # ----不符合预期的词语----
        "漏水", "纯水", "碱水", "水果", "水雾", "酒水", "吸水", "精萃水", "净水", "补水", "花露水", "热水",
        "玻璃水", "cm", "ml", "ML", "口水", "椰子水", "缩水", "水龙", "水润", "水牛", "水枪", "香水", "柠檬水",
    ]
    lowBlackList = [
        "多拍", "返红包", "券包", "免单", "预售", "试用", "点秒杀", "前10", "以旧换新", "防身",
        "小程序下单", "直播间下单",
        # ----实物----
        "火锅", "羊肉", "香菇", "烧烤", "麻辣烫", "杯", "馋嘴", "卤", "梨", "粽子", "鲜花", "虾",
        "內衣", "拖鞋", "椅", "洁面", "购物袋", "佛", "洗", "纸", "清风", "蛋白", "豆浆",
        "机油", "猫粮", "婴儿", "小孩", "无线",
        # ----品牌----
        "茅台", "五粮液", "习酒", "窖", "农夫山泉",
        "珀莱雅", "雅诗兰黛", "毛戈平", "屈臣氏",
        "奶茶", "奈雪", "蜜雪", "巧乐兹", "果汁", "麦片", "莓", "特仑苏", "三只松鼠",
        "第三方", "京造", "京东买药", "采销", "东方甄选",
        # ----虚拟----
        "华为", "HUAWEI", "MiPay", "yzf", "翼支付",
        "火车", "电影", "门票", "打车", "单车", "流量", "出行优惠券", "网盘", "地铁", "网易云", "机票", "顺丰", "快递",
        # ----无效----
        "京东plus", "PLUS会员", "Plus拍下", "plus领", "联通", "移动套餐", "美团圈圈", "王卡", "钻石会员",
        "元梦之星", "老乡鸡", "沪上阿姨", "永和大王", "沃尔玛",
    ]
    if any(sub in title for sub in commonBlackList):
        return False
    if any(sub in title for sub in highBlackList):
        return False
    if any(sub in title for sub in lowBlackList):
        return False
    whiteList = [
        "云闪付", "ysf",
        "xyk", "性用卡", "还款",
        "中国银行", "中行", "农业银行", "农行", "交通银行", "交行", "浦发", "邮储", "光大", "兴业",
        "平安", "浙商", "杭州银行", "北京银行", "宁波银行",
        "工商银行", "工商", "工行", "工银", "e生活",
        "建设银行", "建行", "建融", "善融",
        "招商银行", "招行", "掌上生活", "体验金",
        "中信", "动卡空间",
        "微众",
        "淘宝", "tb", "手淘", "天猫", "猫超", "闲鱼", "高德",
        "支付宝", "zfb", "转账", "网商", "某付宝",
        "微信", "wx", "vx", "v.x", "V.x", "小程序", "立减金", "公众号", "原文", "推文",
        "京东", "狗东", "JD", "京豆", "e卡",
        "抖音", "dy",
        "美团", "饿了么", "elm",
        "红包", "抽奖", "秒到", "保底", "游戏", "下载",
        "水",
        # "同程", "携程", "途牛",
        "话费", "移动", "和包", "电信", "Q币", "扣币",
        "麦当劳", "肯德基", "必胜客", "星巴克", "瑞幸", "朴朴", "喜茶", "霸王茶姬", "百果园", "茶百道",
        "礼品卡", "星礼卡", "苹果卡",
        "深圳通", "网上国网",
    ]
    if not any(sub in title for sub in whiteList):
        return False
    content = get_content(href)
    # todo 评论回复
    # print(content)
    for checkItem in commonBlackList:
        if content and checkItem in content.get_text():
            print(checkItem + "----关键字不合法，已忽略" + '\t\t' + href)
            return False
    print(title + '\t\t' + href)
    item = {
        'title': title,
        'href': href,
        'content': content
    }
    xb_list.append(item)


def get_content(href):
    data = requests.get(href)
    data.encoding = 'utf-8'
    soup = BeautifulSoup(data.text, 'html.parser')
    xb_content = soup.select('div.genxin')
    if not xb_content:
        xb_content = soup.select('#xbcontent > p')
    if not xb_content:
        print("获取不到帖子内容")
        return ''
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
    if xb_list:
        content = ''
        for item in xb_list:
            content += f'''
##### [{item['title']}]({item['href']})
{item['content']}
'''
        notify.pushplus_bot_my(xb_list[0]["title"], content)
        with open("xb.md", 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print("暂无线报！！")


if __name__ == '__main__':
    get_top_summary()
    notify_markdown()
