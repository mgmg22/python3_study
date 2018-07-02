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
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/fd8d943c60644147bd8cb0d3d36dc66b/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/e42a103f45354e4d962a3e9e18dabc3d/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/cf25e1f464f943aebad40c62cedf1894/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/68ae7809dac24561a7f422546a1a61bb/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/eb99b871793f489aa51b8c7b54d2e9ac/',
    'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/7e8ca1788a324a9098762a1e04f34ab1/',
]

# 每个成员项目计划首页的位置下标
urlPos = [
    8,
    10,
    9,
    11,
    12,
    7,
]
# 发送钉钉通知时@的成员
ding_mobile = [''] * len(user)
# 每个成员的项目计划首页
plan_home_url = [''] * len(user)
# 项目规划检查结果，0为未写1为写了
check_flag = [0] * len(user)
# 任务即将延期
check_today = [''] * len(user)

ding_header = {
    "Content-Type": "application/json",
    "charset": "utf-8"
}

cookies = {
    'Cookie': 'remember_token=26bcc67f-d848-457a-a9da-11025384b70c;'
              '_tower2_session=507659259737fd575bffd470d9b770b9;'
}
# 当日时间
today = time.strftime("%Y-%m-%d", time.localtime())
# 检查结果
report = ""


# 获取每个人的项目计划url
def get_plan_url():
    data = requests.get(format_url(projectUrl), cookies=cookies)
    soup = BeautifulSoup(data.text, 'lxml')
    home_links = soup.select('div.title > h4 > span.name > a')
    i = 0
    for pos in urlPos:
        plan_home_url[i] = home_links[pos].get('href')
        i = i + 1


# url域名转化
def format_url(str):
    if is_server:
        return str.replace('https://tower.im', 'https://hk.tower.im')
    else:
        return str.replace('https://hk.tower.im', 'https://tower.im')


# 遍历每个人的项目计划url
def get_plan_item():
    for pos in range(0, len(plan_home_url)):
        data = requests.get(format_url(plan_home_url[pos]), cookies=cookies)
        soup = BeautifulSoup(data.text, 'lxml')
        plan_links = soup.select('div.todo-wrap > span.todo-content > span.content-linkable > a')
        # 遍历每个项目url
        for plan_link in plan_links:
            print(pos, "#", plan_link)
            check_data = requests.get(format_url(plan_link.get('href')), cookies=cookies)
            check_soup = BeautifulSoup(check_data.text, 'lxml')
            quick_links = check_soup.select('div.check-item > a.label.check-item-quicklink')
            check_links = check_soup.select('div.event-head > a')
            # 遍历项目中每个检查项的操作时间
            for check_link in check_links:
                if today in check_link.get_text():
                    check_flag[pos] = 1
                    break
            # 判断是否当日任务未标记完成
            for check_item in quick_links:
                if plan_link.select('span.due'):
                    if today in check_item.select('span.due')[0].get_text():
                        # 获取即将延期的检查项名称
                        check_today[pos] += "\n" + check_soup.select(
                            'div.check-item > a.check-item-name > span.check_item-rest')[
                            quick_links.index(check_item)].get_text()
                        check_flag[pos] += 2
                        break


# 检查日报
def check_daily():
    global report
    # 遍历每个日报的url
    for pos in range(len(daily_url)):
        data = requests.get(format_url(daily_url[pos]), cookies=cookies)
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
    if is_server:
        report = datetime.datetime.now().strftime('%H:%M:%S') + '(服务器定时提醒)\n' + report
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
    print(ding_mobile)
    print(data)
    req = requests.post(ding_url, data=ding_data, headers=ding_header)


if __name__ == '__main__':
    check_daily()
    get_plan_url()
    get_plan_item()
    get_check_result()
    send_ding()
