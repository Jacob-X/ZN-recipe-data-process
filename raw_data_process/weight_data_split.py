# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/23 19:23
# @File    : weight_data_split.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re



# def process_unit(x):
#
#     x = str(x)
#     nums = re.findall('\d+', x)
#     ch_nums = re.findall('([一二两三四五六七八九十半]+)', x)
#     unit = re.findall('([勺匙茶匙汤匙ml片斤两杯碗瓶瓣]+)', x)
#     res = 0
#
#     for n in nums:
#         res += int(n)
#     for cn in ch_nums:
#         if len(cn)>1:
#             res += chinese_to_arabic[cn[0]]
#     # for u in units:
#     #     res += unit_to_g[u]
#     return res, unit

def convert_chinese_num(val):
    if isinstance(val, str):
        return chinese_to_arabic.get(val, val)
    return val

    # 转换单位
# def convert_unit(row):
#     if isinstance(row['quantity'], (str, int, float)) and row['unit'] in unit_to_g:
#         try:
#             return int(row['quantity']) * unit_to_g.get(row['unit'], 1)
#         except ValueError:
#             return row['quantity']
#     return row['quantity']



if __name__ == '__main__':

    raw_data = pd.read_csv("struct_food_info.csv")

    # 中文数字到阿拉伯数字的映射
    chinese_to_arabic = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
        '两': 2,
        '半': 0.5,
        '个': 1,
        '只': 1,
        '块': 1,
        '瓣': 1,
        '颗': 1,
        '粒': 1,
        '枚': 1
        # ... 其他数字
    }

    # 单位到g的转换
    unit_to_g = {
        '勺': 5,  # 假设1勺=5g
        '小勺': 5,  # 假设1勺=5g
        '大勺': 15,  # 假设1勺=15g
        "汤勺": 15,  # 假设1勺=15g
        "小匙": 5,  # 假设1勺=5g
        "大匙": 15,  # 假设1勺=15g
        '匙': 5,  # 假设1匙=5g
        '茶匙': 5,  # 假设1匙=5g
        '汤匙': 15,  # 假设1汤匙=15g
        'ml': 1,  # 假设1ml=1g
        '片': 3,  # 假设1片=3g
        '斤': 500,  # 假设1斤=500g
        '两': 50,  # 假设1两=50g
        '杯': 200,  # 假设1杯=200g
        '碗': 300,  # 假设1碗=300g
        '瓶': 500,  # 假设1瓶=500g
        '瓣': 10,  # 假设1瓣=10g
        '小碗': 300,  # 假设1小碗=300g
        # ... 其他单位
    }

    # 把quantity的中文字换成数字
    # raw_data['ingredient_weight'] = raw_data['ingredient_weight'].apply(convert_chinese_num)
    #
    # raw_data.to_csv("num_struct_food_info.csv",index=False)

    split_data =[]
    for index,row in raw_data.iterrows():

        quantity = 0
        unit = ""

        ingredient_weight = row["ingredient_weight"]
        pattern = r'(\d+(\.\d+)?)|([一二两三四五六七八九十百千万半]+)'
        results = re.findall(pattern, ingredient_weight)

        if len(results) != 0:
            for result in results[0]:
                if result != '':
                    quantity = result
                    unit = ingredient_weight.replace(quantity, '')
                    break
        else:
            unit = ingredient_weight

        print(ingredient_weight,quantity,unit)

        split_data.append([row["title"], row["url"], row["ingredient_name"], quantity, unit])

    df_split_data = pd.DataFrame(split_data,columns=["title","url","ingredient_name","quantity","unit"])
    df_split_data.to_csv("split_struct_food_info.csv",index=False)

        # if ingredient_weight == "适量":
