#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/30
# @Author  : browser
# @Software: PyCharm
# @File    : cuttlefish.py


import argparse
import time
import os
import json
import openai
import backoff
from DecryptLogin import login

cid_name: dict = {0: '学前教育', 1: '基础教育', 2: '高校与高等教育', 3: '语言/资格考试', 4: '法律', 5: '建筑', 6: '互联网', 7: '行业资料', 8: '政务民生',
                  9: '商品说明书', 10: '实用模板', 11: '生活娱乐'}

# Set your API key
openai.api_key = "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"


def logging(msg, tip='INFO'):
    """
    日志格式化
    :param msg: 格式化信息
    :param tip: 日志等级
    :return:
    """
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')


def get_login():
    """
    百度扫码登入，返回session
    :return: session
    """
    lg = login.Login()
    infos_return, session = lg.baidu('', '', 'scanqr')
    return session


def parseArgs():
    """
    命令行参数解析
    :return: args
    """
    parser = argparse.ArgumentParser(description='墨斗鱼文章生成')
    parser.add_argument('--refresh', dest='refresh', help='重新获取任务列表', action='store_true')
    args = parser.parse_args()
    return args


class Gater_wool:
    """
    该死，就是想薅一把羊毛，行动起来
    """

    def __init__(self):
        self.sum = 300  # 每天api接口调用上线
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://cuttlefish.baidu.com/shopmis',
            'Accept': '*/*'
        }

    def get_task(self):
        """
        获取墨斗鱼任务列表
        :return: list
        """
        # cid_list: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        cid_list: list = [11]
        pn: int = 0
        rn: int = 20
        task_name = []
        session = get_login()
        for cid in cid_list:
            f_url = f'https://cuttlefish.baidu.com/user/interface/getquerypacklist?cid={cid}&pn={pn}&rn={rn}&word=&tab=1'
            response = session.get(f_url, headers=self.headers)
            response_json = response.json()
            if response_json['status']['code'] != 0:
                logging('%s 第 %s 页，获取任务名失败, 原因: %s' % (cid_name[cid], pn, response_json.get('status')))
            else:
                total = response_json['data']['total']
                logging('total: %s' % total)
                pn = int(total / rn)
                t_pn: int = 0
                while t_pn < pn:
                    t_url = f'https://cuttlefish.baidu.com/user/interface/getquerypacklist?cid={cid}&pn={t_pn}&rn={rn}&word=&tab=1'
                    t_response = session.get(t_url, headers=self.headers)
                    t_response_json = t_response.json()
                    if t_response_json['status']['code'] != 0:
                        logging('%s 第 %s 页，获取任务名失败, 原因: %s' % (cid_name[cid], t_pn, response_json.get('status')))
                    else:
                        # 从响应内容中获取任务名
                        for i in t_response_json['data']['queryList']:
                            task_name.append(i['queryName'])

                        # 判断是否成功
                        if t_response_json['status']['code'] == 0:
                            logging('%s 第 %s 页，获取任务名成功 %s' % (cid_name[cid], t_pn, response_json.get('status')))
                        else:
                            logging('%s 第 %s 页，获取任务名失败, 原因: %s' % (cid_name[cid], t_pn, response_json.get('status')))
                    t_pn += 1
                    time.sleep(1.5)
        # logging('task_name: %s' % task_name)
        return task_name

    def write_to_file(self):
        """
        任务名信息存入文件
        :return: file
        """
        args = parseArgs()
        if args.refresh:
            task_info = self.get_task()
            f = open('../task/task_name.json', 'w', encoding='utf-8')
            json.dump(task_info, f, ensure_ascii=False, indent=4)
            logging('任务名刷新并写入成功!!!')
            f.close()
            return task_info
        elif os.path.exists('../task/task_name.json'):
            f = open('../task/task_name.json', 'r', encoding='utf-8')
            task_info = json.load(f)
            logging('task_info: %s' % task_info)
            logging('任务名成功读取!!!')
            f.close()
            return task_info
        else:
            task_info = self.get_task()
            f = open('../task/task_name.json', 'w', encoding='utf-8')
            json.dump(task_info, f, ensure_ascii=False, indent=4)
            logging('任务名首次写入成功!!!')
            f.close()
            return task_info

    def write_to_docx(self, **kwargs):
        """
        生成docx的word文档
        :return: .docx
        """
        pass

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    def completions_with_backoff(self):
        count_sum = self.sum
        num = 0
        total_task_name = self.write_to_file()
        for name in total_task_name:
            prompt = str(name)
            logging('【%s】 文章生成任务---开始' % name)
            try:
                # Use the ChatGPT model to generate a response to a prompt
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=4000,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                content = response.choices[0].text
                logging('【%s】文章内容生成---已完成' % name)
                self.write_to_docx(content)
                logging('【%s】docx文档生成---已完成' % name)
                time.sleep(30)
            except Exception as e:
                logging('openai接口异常: %s' % e)

            # 每天生成篇数限制
            if num >= count_sum:
                break
            num += 1


if __name__ == '__main__':
    Gater_wool = Gater_wool()
    Gater_wool.write_to_file()
