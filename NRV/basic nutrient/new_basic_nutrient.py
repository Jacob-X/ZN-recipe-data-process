# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/3 14:54
# @File    : new_basic_nutrient.py
# @Software: PyCharm


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':

    # Load the data from the file
    df = pd.read_excel("../pic/animal_nrv_analysis.xlsx")

    # Define the names
    basic_name = ['Energy kJ', 'Protein', 'Fat', 'Carbohydrate']
    vitamin_name = ['Vitamin A', 'Thiamin','Riboflavin', 'Niacin', 'Vitamin B6', 'Folate', 'Vitamin B12','Vitamin C', 'Vitamin D', 'Vitamin K']
    metal_name = ['Calcium', 'Phosphorus','Potassium', 'Sodium', 'Iron', 'Zinc', 'Selenium', 'Copper', 'Iodine']

    # Define the Chinese names
    basic_cn_name = ['能量 * 100', '蛋白质', '脂肪', '碳水化合物']
    vitamin_cn_name = ['维生素A', '维生素B1', '维生素B2', '烟酸', '维生素B6', '叶酸', '维生素B12', '维生素C', '维生素D', '维生素K']
    metal_cn_name = ['钙', '磷', '钾', '钠', '铁', '锌', '硒', '铜', '碘']


    basic_weight = ["千焦","克","克","克"]
    vitamin_weight = ["微克","毫克","毫克","毫克","毫克","微克","微克","毫克","微克","微克"]
    metal_weight = ["毫克","毫克","毫克","毫克","毫克","毫克","微克","毫克","微克"]

    basic_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(basic_cn_name, basic_weight)]
    vitamin_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(vitamin_cn_name, vitamin_weight)]
    metal_cn_name_with_weight = [f'{name} ({weight})' for name, weight in zip(metal_cn_name, metal_weight)]

    # Modify the dictionary to include weights
    dict_basic_name = dict(zip(basic_name, basic_cn_name_with_weight))

    # Create a combined dictionary of names
    # dict_basic_name = dict(zip(basic_name, basic_cn_name))
    dict_vitamin_name = dict(zip(vitamin_name, vitamin_cn_name_with_weight))
    dict_metal_name = dict(zip(metal_name, metal_cn_name_with_weight))

    # Merge all dictionaries into one
    dict_all_names = {**dict_basic_name, **dict_vitamin_name, **dict_metal_name}

    for i in range(df.shape[0]):
    # for i in range(2):
        df_new_single_row = df.iloc[i]

        # Retrieve basic nutrients
        basic_nutrient = df_new_single_row[basic_name]
        vitamin_value = df_new_single_row[vitamin_name]
        metal_value = df_new_single_row[metal_name]

        if df_new_single_row["Energy kJ"] == "—":
            continue
        #
        df_new_single_row['Energy kJ'] = pd.to_numeric(df_new_single_row['Energy kJ'], errors='coerce')
        # Calculate the nutrients for each category and divide the 'Energy kJ' values by 100
        basic_nutrient['Energy kJ'] = basic_nutrient['Energy kJ'] / 100

        # Translate the index to Chinese
        basic_nutrient.index = basic_nutrient.index.map(dict_basic_name)
        vitamin_value.index = vitamin_value.index.map(dict_vitamin_name)
        metal_value.index = metal_value.index.map(dict_metal_name)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        barplot = sns.barplot(x=basic_nutrient.index, y=basic_nutrient.values, palette="viridis")

        # Add labels to the plot
        for p in barplot.patches:
            barplot.annotate(format(p.get_height(), '.1f'),
                             (p.get_x() + p.get_width() / 2., p.get_height()),
                             ha='center',
                             va='center',
                             xytext=(0, 10),
                             textcoords='offset points')

        plt.title(f'基本营养素 '+str(df_new_single_row["Food name"]).replace("/","、")+"(每100g)")
        plt.xlabel('Nutrient')
        plt.ylabel('Value')
        file_path = f'meat/basic_pics/'
        plt.savefig(file_path+str(df_new_single_row["Food code"]) + str(df_new_single_row["Food name"]).replace("/","、") + "基本营养素" + '.png')  # 指定保存的文件名和格式
        # plt.show()

        # plt.figure(figsize=(12, 9))
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        #
        # barplot = sns.barplot(x=vitamin_value.index, y=vitamin_value.values, palette="viridis")
        #
        # # Add labels to the plot
        # for p in barplot.patches:
        #     barplot.annotate(format(p.get_height(), '.1f'),
        #                      (p.get_x() + p.get_width() / 2., p.get_height()),
        #                      ha='center',
        #                      va='center',
        #                      xytext=(0, 10),
        #                      textcoords='offset points')
        #
        # plt.title(f'维生素'+str(df_new_single_row["Food name"]).replace("/","、")+"(每100g)")
        # plt.xlabel('Vitamin')
        # plt.ylabel('Value')
        # plt.xticks(rotation=45)
        # file_path = f'meat/vitamin_pics/'
        # # print(file_path + str(df_new_single_row["Food code"]) + str(df_new_single_row["Food name"]).replace("/","、") + "维生素" + '.png')
        # plt.savefig(file_path + str(df_new_single_row["Food code"]) + str(df_new_single_row["Food name"]).replace("/","、") + "维生素" + '.png')
    #
        # plt.figure(figsize=(12, 9))
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
        # barplot = sns.barplot(x=metal_value.index, y=metal_value.values, palette="viridis")
        #
        # # Add labels to the plot
        # for p in barplot.patches:
        #     barplot.annotate(format(p.get_height(), '.1f'),
        #                      (p.get_x() + p.get_width() / 2., p.get_height()),
        #                      ha='center',
        #                      va='center',
        #                      xytext=(0, 10),
        #                      textcoords='offset points')
        #
        # plt.title(f'矿物质'+str(df_new_single_row["Food name"]).replace("/","、")+"(每100g)")
        # plt.xlabel('Metal')
        # plt.ylabel('Value')
        # plt.xticks(rotation=45)
        # file_path = f'meat/metal_pics/'
        # plt.savefig(file_path + str(df_new_single_row["Food code"]) + str(df_new_single_row["Food name"]).replace("/",
        #                                                                                                           "、") + "矿物质" + '.png')



