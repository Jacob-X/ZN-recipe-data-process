# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/30 16:50
# @File    : ingredient_drop_duplicates.py
# @Software: PyCharm

import pandas as pd

if __name__ == '__main__':
    recipe_info = pd.read_csv("complete_recipe_info.csv")
    ingredient_info = recipe_info.drop_duplicates(subset=['ingredient_name'], keep='first')[['ingredient_name',"food_name_1","food_name_2","food_code"]]

    recipe_info_list = []
    for index,row in recipe_info.iterrows():
        recipe_info_list.append(row.tolist())

    # info 5,6,7
    recipe_complete_info_list = []
    recipe_manually_info_list = []
    for info in recipe_info_list:
        if pd.isna(info[5]) or pd.isna(info[6]) or pd.isna(info[7]):
        # if info[5] == "nan" or info[6] == "nan" or info[7] == "nan":
            recipe_manually_info_list.append([info[2],info[5],info[6],info[7]])
            print("need to change manually: ", info)
            continue
        else:
            recipe_complete_info_list.append(info)

    print("recipe_complete_info_list",len(recipe_complete_info_list))
    print("recipe_manually_info_list",len(recipe_manually_info_list))

    # print(ingredient_info.head())
    ingredient_info.to_csv("drop_duplicates_ingredient_info.csv",index=False)

    # recipe_complete_info_list_df = pd.DataFrame(recipe_complete_info_list,columns=["recipe_id","recipe_name","ingredient_name","quantity","unit","food_name_1","food_name_2","food_code"])
    # recipe_complete_info_list_df.to_csv("recipe_complete_info_list.csv",index=False)

    recipe_manually_info_list = pd.DataFrame(recipe_manually_info_list,columns=["ingredient_name","food_name_1","food_name_2","food_code"])

    recipe_manually_info_list.drop_duplicates(subset=['ingredient_name'], keep='first',inplace=True)

    recipe_manually_info_list.to_csv("ingredient_manually_info_list.csv",index=False)

