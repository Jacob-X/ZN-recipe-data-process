# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/14 14:29
# @File    : manual_data_process.py
# @Software: PyCharm

import pandas as pd
import numpy as np

if __name__ == '__main__':
    manual_data = pd.read_csv("manual.csv")
    print(manual_data.head())
    print(len(manual_data))

    manual_ingredient = manual_data["ingredient"].unique()
    print(len(manual_ingredient))
    # print(manual_ingredient.head())


    manual_df = manual_data.drop_duplicates(subset=['ingredient'], inplace=True)

    print(manual_data.head())

    # manual_df = pd.DataFrame()
    # # for i in range(len(manual_ingredient)):
    # for i in range(10):
    #     print(manual_ingredient[i])
    #     print(manual_data[manual_data["ingredient"] == manual_ingredient[i]])
    #     manual_df.append(manual_data[manual_data["ingredient"] == manual_ingredient[i]])
    #
    # print(manual_df.head())

    manual_data.to_csv("manual_data.csv",index=False)
