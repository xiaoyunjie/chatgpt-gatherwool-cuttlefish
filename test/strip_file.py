#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/10 14:24
# @Author  : Browser
# @File    : strip_file.py
# @Software: PyCharm


def strip_file(old_f_name, new_f_name):
    """remove the space or Tab or enter in a file,and output to a new file in the same folder"""
    fp = open(old_f_name, 'r', encoding='UTF-8')
    new_fp = open(new_f_name, "w")
    for each_line in fp.readlines():
        # newStr = each_line.replace(" ", "").replace("\t", "").strip()
        new_str = each_line.replace("\n", "")
        # print "Write:",newStr
        new_fp.write(new_str)
    fp.close()
    new_fp.close()


if __name__ == "__main__":
    oldName = input("input file name:")
    nameList = oldName.split(".")
    newName = "%s%s%s" % (nameList[0], "_new.", nameList[1])
    strip_file(oldName, newName)
    print("finish output to new file:", newName)

