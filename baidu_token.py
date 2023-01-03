#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29
# @Author  : browser
# @Software: PyCharm
# @File    : baidu_token.py

import requests

# 设置账号密码
username = 'nupt_hot'
password = 'xyjyy20170217'

# 登录并获取 token
login_url = 'https://passport.baidu.com/v2/api/?login'
data = {'username': username, 'password': password}
response = requests.post(login_url, data=data)

# 如果登录成功，response 会返回 token
if response.status_code == 200:
    token = response.json()['token']
    print(f'Successfully logged in and got token: {token}')
else:
    print(f'Failed to login: {response.status_code}')
