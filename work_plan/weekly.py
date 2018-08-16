#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : weekly.py
# @Author: sxs
# @Date  : 2018/7/2
# @Desc  :根据模板生成周报
import calendar
import datetime
import requests
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate, Listing

my_plan_url = 'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/lists/b9dd450e808743de958d450c29f3ebb0/show/'

kpi_url = 'https://tower.im/projects/e4199ea0e86d4c3bb51cce4b12eb0f78/'
context = {
    'month': datetime.datetime.now().month,
    'week': int(datetime.datetime.now().day / 7) + 1,
    'mylisting': Listing('the listing\nwith\nsome\nlines \a and some paragraph \a and special chars : <>&'),
    'tasks': [
        {'name': '付呗重构', 'progress': 10, 'state': '产品会'},
        {'name': '服务化', 'progress': 100, 'state': ''},
    ],
    'plans': [],
}
cookies = {
    'Cookie': 'remember_token=26bcc67f-d848-457a-a9da-11025384b70c;'
              '_tower2_session=507659259737fd575bffd470d9b770b9;'
}


def next_week_plan():
    pass


def save_tpl():
    tpl = DocxTemplate('base_tpl.docx')
    plan = {'name': '付呗重构', 'time': get_next_time()}
    context.get("plans").append(plan)
    tpl.render(context)
    tpl.save('sxs周报.docx')


def get_next_time():
    """
    下周任务-开发时间
    """
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while today.weekday() != calendar.MONDAY:
        today += one_day
    return '{}—{}'.format(today.strftime('%m/%d'), (today + datetime.timedelta(days=4)).strftime('%m/%d'))


def get_my_plan():
    data = requests.get(my_plan_url, cookies=cookies)
    soup = BeautifulSoup(data.text, 'lxml')
    plan_links = soup.select('div.todo-wrap > span.todo-content > span.content-linkable > a')
    print(plan_links)


if __name__ == '__main__':
    save_tpl()
    print(get_next_time())
    # get_my_plan()
