# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 13:00
# @File    : re_test.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import re

if __name__ == '__main__':

    s1 = "甘薯［山芋、红薯］"
    s2 = "甘薯（红心，白心）［山芋、红薯］"
    s_list = [s1,s2]

    s3 = []
    s_list.extend(s3)
    print(s_list)

    # s = "甘薯（红心）［山芋、红薯］"
    for s in s_list:
        s = s.replace("（", "(").replace("）", ")").replace("［", "[").replace("］", "]").replace("，", ",").replace("、", ",")

        if "(" in s or ")" in s:
            pattern1 = r'^(.*?)\('  # 匹配第一个()前的内容
            pattern2 = r'\((.*?)\)'  # 匹配第一个()内的内容
            pattern3 = r'\[(.*)\]'  # 匹配[]内的内容

            match1 = re.findall(pattern1, s)
            match2 = re.findall(pattern2, s)
            match3 = re.findall(pattern3, s)

            ingredient_name = match1[0].strip()
            attach_info = match2[0].split(",")
            alias = match3[0].split(",")

            all_ingredient_name = []

            names = []
            names.append(ingredient_name)
            names.extend(alias)
            # print(names)

            all_ingredient_name.extend(names)
            for name in names:
                for info in attach_info:
                    all_ingredient_name.append(name + info)
                    all_ingredient_name.append(info + name)

            print(all_ingredient_name)

        else:
            pattern1 = r'^(.*?)\['  # 匹配[]前的内容
            pattern2 = r'\[(.*)\]'  # 匹配[]内的内容
            match1 = re.findall(pattern1, s)
            match2 = re.findall(pattern2, s)
            alias = match2[0].split(",")

            ingredient_name = match1[0].strip()
            alias = match2[0].split(",")

            all_ingredient_name = []

            names = []
            names.append(ingredient_name)
            names.extend(alias)
            print(names)





