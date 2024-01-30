# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/7/30 16:13
# @File    : basic_nutrient.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    df_new_single_row = pd.read_excel("../pic/nrv_analysis.xlsx")
    # print(df_new_single_row)

    basic_name = ['Energy kJ', 'Protein', 'Fat', 'Carbohydrate']
    basic_cn_name = ['能量（千卡）', '蛋白质', '脂肪', '碳水化合物']
    dict_basic_name = dict(zip(basic_name, basic_cn_name))

    vitamin_name = ['Vitamin A', 'Thiamin','Riboflavin', 'Niacin', 'Vitamin B6', 'Folate', 'Vitamin B12','Vitamin C', 'Vitamin D', 'Vitamin K']
    vitamin_cn_name = ['维生素A', '维生素B1', '维生素B2', '烟酸', '维生素B6', '叶酸', '维生素B12', '维生素C', '维生素D', '维生素K']
    dict_basic_name = dict(zip(vitamin_name, vitamin_cn_name))

    metal_name = ['Calcium', 'Phosphorus','Potassium', 'Sodium', 'Iron', 'Zinc', 'Selenium', 'Copper', 'Iodine']
    metal_cn_name = [ '钙', '磷', '钾', '钠', '铁', '锌', '硒', '铜', '碘']
    dict_basic_name = dict(zip(metal_name, metal_cn_name))

    basic_weight = ["千焦","克","克","克"]
    vitamin_weight = ["微克","毫克","毫克","毫克","毫克","微克","微克","毫克","微克","微克"]
    metal_weight = ["毫克","毫克","毫克","毫克","毫克","毫克","微克","毫克","微克"]

    basic_nutrient = df_new_single_row[basic_name].copy()
    vitamin_nutrient = df_new_single_row[vitamin_name].copy()
    metal_nutrient = df_new_single_row[metal_name].copy()

    print(basic_nutrient)

    # Plotting bar charts
    # basic_nutrient.plot(kind='bar', title='Basic Nutrients', ylabel='Weight', xlabel='Nutrient', legend=False)
    # plt.xticks(range(len(basic_name)), basic_name)
    # plt.show()
    #
    # vitamin_nutrient.plot(kind='bar', title='Vitamin Nutrients', ylabel='Weight', xlabel='Nutrient', legend=False)
    # plt.xticks(range(len(vitamin_name)), vitamin_name)
    # plt.show()
    #
    # metal_nutrient.plot(kind='bar', title='Metal Nutrients', ylabel='Weight', xlabel='Nutrient', legend=False)
    # plt.xticks(range(len(metal_name)), metal_name)
    # plt.show()

    # for index, row in basic_nutrient.iterrows():
    #     plt.bar(basic_name, row)
    #     plt.xlabel('Nutrient')
    #     plt.ylabel('Value')
    #     plt.title('Basic Nutrient')
    #     plt.show()

    for index, row in vitamin_nutrient.iterrows():
        plt.bar(vitamin_name, row)
        plt.xlabel('Nutrient')
        plt.ylabel('Value')
        plt.title('Vitamin Nutrient')
        plt.show()
    #
    # for index, row in metal_nutrient.iterrows():
    #     plt.bar(metal_name, row)
    #     plt.xlabel('Nutrient')
    #     plt.ylabel('Value')
    #     plt.title('Metal Nutrient')
    #     plt.show()





