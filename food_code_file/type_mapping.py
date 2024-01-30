# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/15 14:51
# @File    : type_mapping.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import csv

if __name__ == '__main__':
    food_data = pd.read_csv("success_mapping_result.csv")
    type_data = pd.read_csv("food_label_data.csv")

    print(food_data.head())
    print(type_data.head())

    print(len(type_data["title"]))

    for row,index in food_data.iterrows():
        for row2,index2 in type_data.iterrows():
            if index["title"] == index2["title"]:
                food_data.loc[row,"type"] = index2["type"]
