#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: sxs
# @Date  : 2018/6/20
# @Desc  : tower日报、项目规划检查
from bs4 import BeautifulSoup
import requests
import time
import json
import datetime

# 项目规划首页
projectUrl = 'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/'
# 钉钉机器人地址
ding_url = "https://oapi.dingtalk.com/robot/send?access_token=1fc402abdd2b7dec04921423b45415687f19dd817d4fdae699ca703e855745d1"
# 标识服务器环境为1
is_server = 0
verify = False
user = [
    ' 沈晓顺 ',
    # xsd
    ' @18296120635 ',
    # lj
    ' @17607185665 ',
    # csx
    ' @15036142572 ',
    # fj
    ' @17605819508 ',
    # db
    ' @15820798016 ',
]
# 钉钉关联的手机号码
user_mobile = [
    '15757179463',
    '18296120635',
    '17607185665',
    '15036142572',
    '17605819508',
    '15820798016',
]
# 日报地址，目前是写死的
daily_url = [
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/486e9a8fea7c46748efdbcda13e3d846/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/04fbd653c4a0441eb6e0c1ab281802ab/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/03a7cd7d66bf45cd88196f2053dc31ee/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/7364d59e0d334b518e00ea9f8e596439/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/9ef753698689472eb7bf1cd45e8e9ae4/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/65f79da2687e4d47a3c085841ccbbfa6/',
]
# 每个成员的项目计划首页
plan_home_url = [
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/b9dd450e808743de958d450c29f3ebb0/show/',
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/81e8d620cf914b65843582869155d4b1/show/',
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/795c36f6c0594329a6502b254dbbae1a/show/',
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/1a24c7ef701040f7b6f82bb982acb6b2/show/',
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/f3f3a87ec2f94671b62f6a77768dff94/show/',
    'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/50ee90a6302c47c3be8c39906ece1dc9/show/',
]
# 发送钉钉通知时@的成员
ding_mobile = [''] * len(plan_home_url)
# 项目规划检查结果，0为未写1为写了
check_flag = [0] * len(plan_home_url)
# 任务即将延期
check_today = [''] * len(plan_home_url)

ding_header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}

cookies = {
    'Cookie': 'remember_token=26bcc67f-d848-457a-a9da-11025384b70c;'
              '_tower2_session=6e815a4fb688cf0ef6e6f4bc43fd89a4;'
}
# 当日时间
today = time.strftime("%Y-%m-%d", time.localtime())
# 检查结果
report = ""
# 脚本执行开始时间
start_time = datetime.datetime.now()

session = requests.session()


# url域名转化
def format_url(str):
    if is_server:
        return str.replace('https://tower.im', 'https://hk.tower.im')
    else:
        return str.replace('https://hk.tower.im', 'https://tower.im')


# 遍历每个人的项目计划url
def get_plan_item():
    for pos in range(0, len(plan_home_url)):
        data = session.get(format_url(plan_home_url[pos]), verify=verify)
        soup = BeautifulSoup(data.text, 'lxml')
        plan_links = soup.select('div.todo-wrap > span.todo-content > span.content-linkable > a')
        # 遍历每个项目url
        for plan_link in plan_links:
            print(pos, "#", plan_link)
            check_data = session.get(format_url(plan_link.get('href')), verify=verify)
            check_soup = BeautifulSoup(check_data.text, 'lxml')
            quick_links = check_soup.select('div.check-item > a.label.check-item-quicklink')
            check_links = check_soup.select('div > div.event-head > a')
            # 遍历项目中每个检查项的操作时间
            for check_link in check_links:
                if today in check_link.get_text():
                    check_flag[pos] = 1
                    break
            # 判断是否当日任务未标记完成
            for index, check_item in enumerate(quick_links):
                if check_item.select('span.due'):
                    if today in check_item.select('span.due')[0].get_text():
                        # 获取即将延期的检查项名称
                        check_today[pos] += "\n" + check_soup.select(
                            'div.check-item > a.check-item-name > span.check_item-rest')[index].get_text()
                        check_flag[pos] += 2


# 检查日报
def check_daily():
    global report
    # 遍历每个日报的url
    for pos in range(len(daily_url)):
        data = session.get(format_url(daily_url[pos]), cookies=cookies, verify=verify)
        soup = BeautifulSoup(data.text, 'lxml')
        links = soup.select('div.comment-main > div.info > a.create-time')
        if links:
            if today in str(links[-1]):
                pass
            else:
                ding_mobile[pos] = user_mobile[pos]
                report += user[pos] + "日报还没写" + "\n"


# 输出检查结果
def get_check_result():
    global report
    for index in range(len(check_flag)):
        if check_flag[index] == 0:
            ding_mobile[index] = user_mobile[index]
            report += user[index] + '今日项目规划还未写' + "\n"
        if check_flag[index] >= 2:
            ding_mobile[index] = user_mobile[index]
            report += user[index] + check_today[index] + '检查项任务即将延期' + "\n"


# 同步钉钉机器人
def send_ding():
    global report
    if report is None:
        print(today + "日报都写了")
        return
    # 钉钉@数量超过5个时第6个会失效，第一个@
    if ding_mobile[0] == user_mobile[0] or ding_mobile[0] == '':
        del ding_mobile[0]
    report = '脚本耗时{}秒\n'.format((datetime.datetime.now() - start_time).seconds) + report
    data = {
        "msgtype": "text",
        "text": {
            "content": today + "日报提醒" + "\n" + report
        },
        "at": {
            "atMobiles": ding_mobile
        }
    }
    ding_data = json.dumps(data)
    print('@的人：', ding_mobile)
    print("通知数据：", data)
    requests.post(ding_url, data=ding_data, headers=ding_header)


if __name__ == '__main__':
    check_daily()
    get_plan_item()
    get_check_result()
    send_ding()
