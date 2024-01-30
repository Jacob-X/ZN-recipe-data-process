# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/6 23:01
# @File    : food_code_weight.py
# @Software: PyCharm
from datetime import datetime

import pandas as pd
from datetime import datetime
import re


def process_unit(x):

    x = str(x)
    nums = re.findall('\d+', x)
    ch_nums = re.findall('([一二两三四五六七八九十半]+)', x)
    unit = re.findall('([勺匙茶匙汤匙ml片斤两杯碗瓶瓣]+)', x)
    res = 0

    for n in nums:
        res += int(n)
    for cn in ch_nums:
        if len(cn)>1:
            res += chinese_to_arabic[cn[0]]
    # for u in units:
    #     res += unit_to_g[u]
    return res, unit

def convert_chinese_num(val):
    if isinstance(val, str):
        return chinese_to_arabic.get(val, val)
    return val

    # 转换单位
def convert_unit(row):
    if isinstance(row['quantity'], (str, int, float)) and row['unit'] in unit_to_g:
        try:
            return int(row['quantity']) * unit_to_g.get(row['unit'], 1)
        except ValueError:
            return row['quantity']
    return row['quantity']


if __name__ == '__main__':
    #
    # # Reading the "extended" sheet from the Excel file
    df = pd.read_excel("food_code_1_sort.xlsx", sheet_name="extended")

    print(df.head())

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
    df['quantity'] = df['quantity'].apply(convert_chinese_num)

    # 把unit的中文字换成数字，提取单位进行转换

    # for index, row in df.iterrows():
    #     quantity, unit = process_unit(str(row['unit']))
    #     if quantity != 0:
    #         print(quantity, unit)
    #         row['quantity'] = quantity
    #         row['unit'] = unit
    #     print(row['quantity'],row['unit'])

    # 转换单位
    df['quantity'] = df.apply(convert_unit, axis=1)
    # 克转换成g
    df['unit'] = df['unit'].apply(lambda x: 'g' if x in unit_to_g else x)

    for index, row in df.iterrows():
        if row["unit"] == "克":
            df.at[index, 'unit'] = 'g'

    df.to_csv('raw_food_code_weight.csv', index=False)

    # 针对每一个food_code_1，计算一个中位数
    food_code_list = df["ingredient"].unique().tolist()

    food_code_weight = {}

    for food_code in food_code_list:
        print(food_code)
        food_data = df[df["ingredient"] == food_code]
        food_data = food_data[food_data['unit'] == 'g']
        food_data = food_data[food_data['quantity'].apply(type) != datetime]
        food_data = food_data[food_data['quantity'].apply(type) != str]
        # food_data = food_data[food_data['quantity'].apply(type) == float]


        for index, row in food_data.iterrows():
            if isinstance(row['quantity'], pd.Timestamp):
                food_data.drop(index, inplace=True)
        print(food_data.values)

        median_weight = food_data[food_data['unit'] == 'g']['quantity'].median()
        food_code_weight[food_code] = median_weight

    print(food_code_weight)


    df_data = pd.DataFrame(food_code_weight.items(), columns=['ingredient', 'weight'])
    df_data.to_csv("single_food_name_weight_2.csv", index=False)








    # 对于“适量”的处理
    # for index, row in df[df['unit'] == '适量'].iterrows():
    #     median_weight = df[(df['food_code_1'] == row['food_code_1']) & (df['unit'] == 'g') & df['quantity'].apply(
    #         lambda x: isinstance(x, float))]['quantity'].median()
    #     df.at[index, 'quantity'] = median_weight
    #     df.at[index, 'unit'] = 'g'


    # df.to_csv('food_code_weight_1.csv', index=False)

    # print(df.head(20))
