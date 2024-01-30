# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 18:29
# @File    : food_code_mapping_by_extract_data.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import re


if __name__ == '__main__':

    food_code = pd.read_csv("food_code_unique.csv")
    raw_data = pd.read_csv("../split_struct_food_info.csv")

    food_code_list = []
    for index,row in food_code.iterrows():
        food_code_list.append(row.to_list())

    raw_data_list = []
    for index,row in raw_data.iterrows():
        raw_data_list.append(row.tolist())

    for row in raw_data_list:
        mapping_flag = False
        for code in food_code_list:
            if row[2] == code[0]:
                row.extend(code[1:])
                mapping_flag = True
                break
        if not mapping_flag:
            row.extend(["","",""])

        print(row)

    mapping_data = pd.DataFrame(raw_data_list,columns=['title','url','ingredient_name','quantity','unit','food_name_1',"food_name_2",'food_code'])
    mapping_data.to_csv("food_code_success_mapping.csv",index=False,encoding='utf-8-sig')



