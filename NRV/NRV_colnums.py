# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/10/4 15:26
# @File    : NRV_colnums.py
# @Software: PyCharm
import pandas as pd

if __name__ == '__main__':
    animal = pd.read_excel("./pic/animal_nrv_analysis.xlsx")
    colnums_name = animal.columns.tolist()

    name_list = []
    for name in colnums_name:
        name = name.replace(" ","_")
        name_list.append(name)

    print(name_list)