# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 18:13
# @File    : food_code_extract.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re


if __name__ == '__main__':
    raw_data = pd.read_excel("food_code_1.xlsx")

    food_code = raw_data.drop_duplicates(subset=['ingredient_v'], keep='first')

    food_code = food_code[['ingredient_v','ingredient_vv','food_name','food_code_1']]

    food_code.to_csv("food_code_unique.csv",index=False,encoding='utf-8-sig')

