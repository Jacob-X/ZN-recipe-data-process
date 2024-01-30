# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/25 16:47
# @File    : complete_recipe_info.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import re
from tqdm import tqdm

if __name__ == '__main__':
    complete_recipe_url= pd.read_csv("recipe_integrity_check.csv")
    mapping_result = pd.read_csv("success_mapping_result.csv")
    raw_recipe_info = pd.read_csv("drop_duplicates_recipe_info_data.csv")

    # print(complete_recipe_url.head())
    # print(mapping_result.head())
    # print(raw_recipe_info.head())
    # print(raw_recipe_info.columns)
    # print(raw_recipe_info.loc[0])

    # 完整的url列表
    print("完整的url列表")
    url_list = []
    for index,row in tqdm(complete_recipe_url.iterrows()):
        url_list.append(row["url"])

    # 所有完整菜谱数据的列表
    print("所有完整菜谱数据的列表")
    complete_recipe_list = []
    for index,row in tqdm(mapping_result.iterrows()):
        if row["url"] in url_list:
            complete_recipe_list.append(row.tolist())

    # 根据url去重
    raw_recipe_info = raw_recipe_info.drop_duplicates(subset=['url'], keep='first')



    # 加上菜系标签和四种属性标签
    print("加上菜系标签和四种属性标签")
    url_label_type_list = []
    for index, row in tqdm(raw_recipe_info.iterrows()):
        raw_url = row['url']
        pattern_1 = re.compile(r"'(.*)'")
        url_match = pattern_1.search(raw_url)
        if url_match:
            url = url_match.group(1).split()[1].strip("'")

            raw_labels = row['lable']
            processed_label_list = []
            pattern_2 = r"\['lable', \[(.*)\]\]"
            label_list = re.findall(pattern_2, raw_labels)[0].split(",")
            for label in label_list:
                label = label.strip("(").strip("'").strip(")")
                label = label.replace("(", "")
                label = label.replace("'", "")
                label = label.replace(" ", "")
                processed_label_list.append(label)

            # 四种类别的数据，暂时没加上
            raw_type_list = row['type_list']
            pattern_3 = r"\['type_list', \[(.*)\]\]"
            processed_type_list = []  # ['口味', '原味', '工艺', '煮', '耗时', '十分钟', '难度', '普通']
            type_list = re.findall(pattern_3, raw_type_list)[0].split(",")
            for type in type_list:
                type = type.strip("(").strip("'").strip(")")
                type = type.replace("(", "")
                type = type.replace("'", "")
                type = type.replace(" ", "")
                processed_type_list.append(type)


            url_label_type_list.append([url, processed_label_list,processed_type_list])


    # 给complete_recipe_list加上 type 和 label
    print("给complete_recipe_list加上 type 和 label")
    for recipe in tqdm(complete_recipe_list):
        for info in url_label_type_list:
            if recipe[1] == info[0]:
                recipe.append(info[1])
                recipe.append(info[2])
                print(recipe)
                break

    df_complete_recipe_list = pd.DataFrame(complete_recipe_list, columns=["title", "url", "ingredient_name", "quantity", "unit", "food_name_1", "food_name_2","food_code", "label","type"])
    df_complete_recipe_list.to_csv("complete_recipe_info.csv", index=False, encoding="utf-8-sig")

















