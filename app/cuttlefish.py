#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/30
# @Author  : browser
# @Software: PyCharm
# @File    : cuttlefish.py

import time
from DecryptLogin import login


def logging(msg, tip='INFO'):
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')


def get_login():
    lg = login.Login()
    infos_return, session = lg.baidu('', '', 'scanqr')
    return session


cid_name: dict = {0: '学前教育', 1: '基础教育', 2: '高校与高等教育', 3: '语言/资格考试', 4: '法律', 5: '建筑', 6: '互联网', 7: '行业资料', 8: '政务民生',
                  9: '商品说明书', 10: '实用模板', 11: '生活娱乐'}


class Gater_wool:
    def __init__(self):
        self.session = get_login()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://cuttlefish.baidu.com/shopmis',
            'Accept': '*/*'
        }

    def get_task(self):
        # cid_list: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        cid_list: list = [1]
        pn: int = 0
        rn: int = 20
        task_name = []
        for cid in cid_list:
            f_url = f'https://cuttlefish.baidu.com/user/interface/getquerypacklist?cid=${cid}&pn=${pn}&rn=${rn}&word=&tab=1'
            response = self.session.get(f_url, headers=self.headers)
            response_json = response.json()
            if response_json['status']['code'] != 0:
                logging('%s 第 %s 页，获取任务名失败, 原因: %s' % (cid_name[cid], pn, response_json.get('status')))
            else:
                print('response_json: %s' % response_json)
                total = response_json['data']['total']
                print('total: %s' % total)
                pn = int(total / rn)
                t_pn: int = 0
                while t_pn <= pn:
                    t_url = f'https://cuttlefish.baidu.com/user/interface/getquerypacklist?cid=${cid}&pn=${t_pn}&rn=${rn}&word=&tab=1'
                    t_response = self.session.get(t_url, headers=self.headers)
                    t_response_json = t_response.json()
                    t_pn += 1
                    # 从响应内容中获取任务名
                    for i in t_response_json['data']['queryList']:
                        task_name.append(i['queryName'])

                    # 判断是否成功
                    if t_response_json['status']['code'] == 0:
                        logging('%s 第 %s 页，获取任务名成功 %s' % (cid_name[cid], t_pn, response_json.get('status')))
                    else:
                        logging('%s 第 %s 页，获取任务名失败, 原因: %s' % (cid_name[cid], t_pn, response_json.get('status')))
                    time.sleep(1)
        logging('task_name: %s' % task_name)


if __name__ == '__main__':
    Gater_wool = Gater_wool()
    Gater_wool.get_task()
