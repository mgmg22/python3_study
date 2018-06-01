# tower日报、项目规划检查
# shenxs@fshows.com
from bs4 import BeautifulSoup
import requests
import time
import json

# 项目规划首页
projectUrl = 'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/'
# 钉钉机器人地址
ding_url = "https://oapi.dingtalk.com/robot/send?access_token=1fc402abdd2b7dec04921423b45415687f19dd817d4fdae699ca703e855745d1"

user = [
    ' 沈晓顺 ',
    ' @18296120635 ',
    ' @17607185665 ',
    ' @17605819508 ',
    ' @15036142572 ',
    ' @15820798016 ',
]
# 钉钉关联的手机号码
user_mobile = [
    '15757179463',
    '18296120635',
    '17607185665',
    '17605819508',
    '15036142572',
    '15820798016',
]
# 日报地址，目前是写死的
daily_url = [
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/e36fbb2a93db43a3bb934bf64cddc46b/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/4f90802f997248e1a1f2ac3d232d5220/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/37f7e52806c04e0e914e452e8beb9a36/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/2af574c4b806406f817ccccf7272aeaa/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/7e4c79b39e764fdeb4c262156247f2f5/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/2735ce7f6e984ce7a684c1b7f98cb8d1/',
]

# 每个成员项目计划首页的位置下标
urlPos = [
    8,
    10,
    9,
    10,
    11,
    7,
]
# 发送钉钉通知时@的成员
ding_mobile = [''] * len(user)
# 每个成员的项目计划首页
plan_home_url = [''] * len(user)
# 项目规划检查结果，0为未写1为写了
check_flag = [0] * len(user)
# 任务即将延期
check_quicklink = [0] * len(user)

ding_header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}

headers = {
    'Host': 'tower.im',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://tower.im/users/sign_in',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'intercom-lou-vgeb94xf=1; intercom-id-vgeb94xf=546b02a0-1fc5-4f33-ba45-7393cb139cc6; _ga=GA1.2.2059481265.1510972641; intercom-lou-xbtsuf77=1; _gid=GA1.2.109886700.1525678234; _tower2_session=512d4e4dabfcd4e5c00fd8d430e974a3; _gat=1; _gat_teamTracker=1; intercom-session-xbtsuf77=eXRZeHpadkdMNkF0ekY5UnMvLytONU9wTHZjOUJhaGlkK1dqUXFmYXdRVXQ3M3AzTFVVSXVsd21SZkdoZ1lVRC0tTU1EZFplRVh1ZXhlOW43TDdLZnQrZz09--328d5d9f8a9a12659000a7efd238d4164448d7b8; remember_token=26bcc67f-d848-457a-a9da-11025384b70c'
}
today_result = ""


# 获取每个人的项目计划url
def get_plan_url():
    data = requests.get(projectUrl, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    home_links = soup.select('div.title > h4 > span.name > a')
    i = 0
    for pos in urlPos:
        plan_home_url[i] = home_links[pos].get('href')
        i = i + 1


# url域名转化
def format_url(str):
    return str.replace('https://hk.tower.im', 'https://tower.im')


# 遍历每个人的项目计划url
def get_plan_item():
    for pos in range(0, len(plan_home_url)):
        data = requests.get(format_url(plan_home_url[pos]), headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')
        plan_links = soup.select('div.todo-wrap > span.todo-content > span.content-linkable > a')
        # 遍历每个项目url
        for index, item in enumerate(plan_links):
            print(pos, "#", item)
            check_data = requests.get(format_url(item.get('href')), headers=headers)
            check_soup = BeautifulSoup(check_data.text, 'lxml')
            check_item_quicklinks = check_soup.select('div.check-item > a.label.check-item-quicklink > span.due')
            check_links = check_soup.select('div.event-head > a')
            # 遍历项目中每个检查项的操作时间
            for ind in range(len(check_links)):
                if today in check_links[ind].get_text():
                    check_flag[pos] = 1
                    break
            # 判断是否当日任务未标记完成
            for quicklink_pos in range(len(check_item_quicklinks)):
                if today in check_item_quicklinks[quicklink_pos].get_text():
                    # 获取即将延期的检查项名称
                    check_quicklink[pos] = \
                        check_soup.select('div.check-item > a.check-item-name > span.check_item-rest')[
                            quicklink_pos].get_text()
                    check_flag[pos] = 2
                    break
            # 如果当日任务未标记完成则跳出检查项遍历
            if check_flag[pos] == 2:
                break


# 检查日报
def check_daily():
    global today_result
    # 遍历每个日报的url
    for pos in range(0, len(daily_url)):
        data = requests.get(daily_url[pos], headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')
        links = soup.select('div.comment-main > div.info > a:nth-of-type(2)')
        # 局部变量1未写0已写
        daily = 1
        for index, item in enumerate(links):
            if today in item.get('title'):
                daily = 0
        if daily == 1:
            ding_mobile[pos] = user_mobile[pos]
            today_result += user[pos] + "日报还没写" + "\n"


# 输出检查结果
def get_check_result():
    global today_result
    for index in range(len(check_flag)):
        if check_flag[index] == 0:
            ding_mobile[index] = user_mobile[index]
            today_result += user[index] + '今日项目规划还未写' + "\n"
            print(user[index] + '今日项目规划还未写' + "\n")
        if check_flag[index] == 2:
            ding_mobile[index] = user_mobile[index]
            today_result += user[index] + check_quicklink[index] + '检查项任务即将延期' + "\n"


# 同步钉钉机器人
def send_ding():
    if today_result == '':
        print(today + "日报都写了")
        return
    # 钉钉@数量超过5个时第6个会失效，第一个@
    if ding_mobile[0] == user_mobile[0] or ding_mobile[0] == '':
        del ding_mobile[0]
    data = {
        "msgtype": "text",
        "text": {
            "content": today + "日报提醒" + "\n" + today_result
        },
        "at": {
            "atMobiles": ding_mobile
        }
    }
    ding_data = json.dumps(data)
    print(ding_mobile)
    req = requests.post(ding_url, data=ding_data, headers=ding_header)


if __name__ == '__main__':
    # 当日时间
    today = time.strftime("%Y-%m-%d", time.localtime())
    check_daily()
    get_plan_url()
    get_plan_item()
    get_check_result()
    send_ding()
