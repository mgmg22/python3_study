import requests
from bs4 import BeautifulSoup
import time
import json

diary_home_url = 'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/lists/3593325114fa41348025e83e2579d1c4/show/'
my_diary = 'https://tower.im/projects/122a4eafcf1643f6bec2bba9d776fc7f/todos/e36fbb2a93db43a3bb934bf64cddc46b/comments'
test_url = 'https://tower.im/projects/29fa2bc07a984a84aed9e3593d507c25/todos/aaf2644e670f4695ae2c1f80a977be04/comments'

headers = {
    'Host': 'tower.im',
    'X-CSRF-Token': 'PpUJq3OjVl2Zcs/e+Ju6odouk7HNgWRx7MThbvzu/cJ/l8ZrPAPbY9tMDc7felvoai1HSa3gZIqYnbg/4Z1wZw==',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'intercom-lou-vgeb94xf=1; intercom-id-vgeb94xf=546b02a0-1fc5-4f33-ba45-7393cb139cc6;'
              ' _ga=GA1.2.2059481265.1510972641; intercom-lou-xbtsuf77=1; '
              'remember_token=26bcc67f-d848-457a-a9da-11025384b70c;'
              ' remember_team_guid=54a02ee4e32f4c1a83abd5445ecd9e05; '
              '_gid=GA1.2.346202964.1529368405; _tower2_session=507659259737fd575bffd470d9b770b9;'
              ' _gat=1; _gat_teamTracker=1; '
              'intercom-session-xbtsuf77=VHBodWs0Q00xTnZyYzNQUG1CcW9Xb2VQekptUkl5eFBBck5lMTZOd0xXM004S2xsSWZ5QnA0M3JKa3I0Z0ptcC0tV29qNHhoMUg4NFJQb2pEVVlTK2NyQT09--ee29ac5b4de10ecfa29068df8dfc318f37eee62a'
}
my_diary_data = {
    '已完成:': '',
    '进行中:': '',
    '未完成:': '',
    '明日任务:': '',
}
my_diary_request = {
    'conn_guid': '7fdb35b9-c834-4d5c-9493-223a5a9720b1',
    'is_html': 1,
    'cc_guids': '',
    'attach_guids': '',
    'delete_attach_guids': '',
    'attach_order': ''
}

username = {'但彬': '', '徐善栋': '', '曹世鑫': '', '方俊': '', '李杰': '', '沈晓顺': ''}
# 当日时间
today = time.strftime("%Y-%m-%d", time.localtime())


def get_diary_url():
    diary_result = requests.get(diary_home_url, headers=headers)
    soup = BeautifulSoup(diary_result.text, 'lxml')
    home_links = soup.select('div.todo-wrap')
    for item in home_links:
        for key in username:
            if key in item.get_text():
                username[key] = item.select('span.todo-content > span.content-linkable > a')[0].get('href')


# 检查日报完成情况
def check_diary():
    get_diary_url()
    for key in username:
        user_diary = requests.get(username.get(key), headers=headers)
        soup = BeautifulSoup(user_diary.text, 'lxml')
        write_time = soup.select('div.comment-main > div.info > a.create-time')
        if today in str(write_time[- 1]):
            username[key] = ''
        else:
            username[key] = '日报没写'
    print(username)


# 写日报
def write_my_diary():
    for key in my_diary_data:
        print(key)
        my_diary_data[key] = input()
    my_diary_request['comment_content'] = format_to_html(my_diary_data)
    result = requests.post(my_diary, headers=headers, data=my_diary_request)
    if result.status_code == 200:
        print(today, '日报发送成功')
    else:
        print(today, '日报发送失败')


# 日报内容转成html
def format_to_html(data):
    html = '<p>{}</p>'.format(today + "日报")
    for key in data.keys():
        html += "<p>{0}</p><p>{1}</p>".format(key, data.get(key))
    return html


if __name__ == '__main__':
    # check_diary()
    write_my_diary()
