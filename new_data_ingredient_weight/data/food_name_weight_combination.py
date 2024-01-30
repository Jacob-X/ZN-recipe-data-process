# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 21:10
# @File    : food_name_weight_combination.py
# @Software: PyCharm

import pandas as pd

if __name__ == '__main__':

    name_weight_1 = pd.read_csv("single_food_name_weight_1.csv")
    name_weight_2 = pd.read_csv("single_food_name_weight_2.csv")
    print(len(name_weight_1))
    print(len(name_weight_2))

    name_weight = pd.concat([name_weight_1,name_weight_2])

    print(len(name_weight))

    name_weight.to_csv("single_food_name_weight.csv",index=False)