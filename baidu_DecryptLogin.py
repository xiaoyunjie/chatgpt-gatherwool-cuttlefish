#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/30
# @Author  : browser
# @Software: PyCharm
# @File    : baidu_DecryptLogin.py

from DecryptLogin import login

lg = login.Login()
infos_return, session = lg.baidu('', '', 'scanqr')
print("infos_return： %s" % infos_return)
