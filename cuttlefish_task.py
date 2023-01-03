#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29
# @Author  : browser
# @Software: PyCharm
# @File    : cuttlefish_task.py


import requests

# 墨斗鱼文库创作中心的API地址
api_url = "https://api.modoufish.com/api/v1/tasks"

# 设置请求头
headers = {
    "Authorization": "YOUR_AUTHORIZATION_TOKEN"
}

# 发送GET请求
response = requests.get(api_url, headers=headers)

# 获取响应内容
data = response.json()

# 从响应内容中获取任务名
task_names = [task["name"] for task in data["data"]]

print(task_names)
