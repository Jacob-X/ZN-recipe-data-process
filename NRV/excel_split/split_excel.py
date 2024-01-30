# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/3 16:42
# @File    : split_excel.py
# @Software: PyCharm


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':

    # Load the data from the file
    df = pd.read_excel("../pic/nrv_analysis.xlsx")

    # Define the names
    basic_name = ["Food code", "Food name", 'Energy kJ', 'Protein', 'Fat', 'Carbohydrate']
    vitamin_name = ["Food code", "Food name", 'Vitamin A', 'Thiamin','Riboflavin', 'Niacin', 'Vitamin B6', 'Folate', 'Vitamin B12','Vitamin C', 'Vitamin D', 'Vitamin K']
    metal_name = ["Food code", "Food name", 'Calcium', 'Phosphorus','Potassium', 'Sodium', 'Iron', 'Zinc', 'Selenium', 'Copper', 'Iodine']

    # Define the Chinese names
    basic_cn_name = ['食物编码','食物名称','能量', '蛋白质', '脂肪', '碳水化合物']
    vitamin_cn_name = ['食物编码','食物名称','维生素A', '维生素B1', '维生素B2', '烟酸', '维生素B6', '叶酸', '维生素B12', '维生素C', '维生素D', '维生素K']
    metal_cn_name = ['食物编码','食物名称','钙', '磷', '钾', '钠', '铁', '锌', '硒', '铜', '碘']

    basic_weight = [' ',' ',"千焦","克","克","克"]
    vitamin_weight = [' ',' ',"微克","毫克","毫克","毫克","毫克","微克","微克","毫克","微克","微克"]
    metal_weight = [' ',' ',"毫克","毫克","毫克","毫克","毫克","毫克","微克","毫克","微克"]

    basic_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(basic_cn_name, basic_weight)]

    # print(basic_cn_name_with_weight)
    vitamin_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(vitamin_cn_name, vitamin_weight)]
    metal_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(metal_cn_name, metal_weight)]

    # Modify the dictionary to include weights
    dict_basic_name = dict(zip(basic_name, basic_cn_name_with_weight))
    dict_vitamin_name = dict(zip(vitamin_name, vitamin_cn_name_with_weight))
    dict_metal_name = dict(zip(metal_name, metal_cn_name_with_weight))

    df_basic = df[basic_name]
    df_vitamin = df[vitamin_name]
    df_metal = df[metal_name]

    df_basic.rename(columns=dict_basic_name, inplace=True)
    df_vitamin.rename(columns=dict_vitamin_name,inplace=True)
    df_metal.rename(columns=dict_metal_name,inplace=True)

    # print(df_basic)

    # df_basic.to_csv("animal_基本营养素.csv",index=False)
    # df_vitamin.to_csv("animal_维他命.csv",index=False)
    # df_metal.to_csv("animal_矿物质.csv",index=False)

    df_basic.to_csv("plant_基本营养素.csv",index=False)
    df_vitamin.to_csv("plant_维他命.csv",index=False)
    df_metal.to_csv("plant_矿物质.csv",index=False)




