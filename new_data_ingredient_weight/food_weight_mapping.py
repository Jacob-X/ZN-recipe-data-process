# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/8 9:58
# @File    : food_weight_mapping.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import csv
from tqdm import tqdm


def list_to_csv(filename,row_list):
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(row_list)

if __name__ == '__main__':

    # raw_food_code = pd.read_excel('food_code_1_sort.xlsx', sheet_name='extended')

    # TODO: 把raw_food_code_weight 里面的内容全部定量化
    #  然后再把全部定量化的数据mapping到food_code_1_sort.xlsx里面
    raw_food_code_weight = pd.read_csv('data/food_code_standard_weight.csv')
    # raw_food_code_weight = pd.read_csv('test.csv')
    # raw_food_code_weight = pd.read_csv("left_unprocessed_data.csv")
    # 拿下面这两个数据进行比对填充，先用名字比对一遍，在用code比对一遍
    single_food_name_weight = pd.read_csv('data/single_food_name_weight_2.csv')
    single_food_code_weight = pd.read_csv('data/single_food_code_weight.csv')
    # df_hand = pd.DataFrame()

    manual_file_name = "manual.csv"

    for index,row in tqdm(raw_food_code_weight.iterrows()):
        # 从ingredient里面找到对应的weight
        print("quantity",row["quantity"],"unit",row["unit"],"ingredient_name",row["ingredient_name"])
        if row["quantity"] != 0 and row["unit"] == "g":
            print("success change", row.tolist())
            list_to_csv("success_mapping_result.csv", [row.tolist()])
            continue
        else:
            # 没有名称的是页面的乱码，直接不要
            if pd.isna(row["ingredient_name"]):
                continue
            else:
                weight = single_food_name_weight[single_food_name_weight["ingredient_name"] == row["ingredient_name"]]["weight"]
                # print("ingredient里面有",weight.values[0],type(weight.values[0]),row["ingredient"])
                # print(weight)

                if np.isnan(weight.values[0]):
                    # 从food_code_1里面找到对应的weight
                    # 要考虑没有foodcode的情况
                    # print(str(row["food_code_1"]))
                    # print(type(row["food_code_1"]))
                    if str(row["food_code"]) == "nan":
                        print("need to change manually: ", row.tolist())
                        list_to_csv(manual_file_name, [row.tolist()])
                        continue
                    else:
                        weight = single_food_code_weight[single_food_code_weight["food_code_1"] == row["food_code"]]["weight"]

                        # 名字和code都找不到，单独保存下来，需要手动处理
                        if np.isnan(weight.values[0]):

                            print("need to change manually: ",row.tolist())
                            list_to_csv(manual_file_name,[row.tolist()])

                            # df_hand = df_hand.append(row)
                            continue

                # 这里是匹配到食材的情况
                if row["unit"] != "g":
                    row["quantity"] = weight.values[0]
                    row["unit"] = "g"
                    # print(row)

                list_to_csv("success_mapping_result.csv", [row.tolist()])
                print("success change",row.tolist())

    # df_hand.to_csv("df_hand.csv",index=False)
    # raw_food_code_weight.to_csv("food_weight_mapping_result.csv",index=False)





        #
        # if row["unit"] != "g":
        #     for index2,row2 in single_food_name_weight.iterrows():
        #         if row["name"] == row2["name"]:
        #             raw_food_code_weight.loc[index,"weight"] = row2["weight"]
        #             raw_food_code_weight.loc[index, "unit"] = row2["unit"]
        #             break

    # print(raw_food_code_weight.head())
    # print("+++"*10)
    # print(single_food_name_weight.head())
    # print("+++" * 10)
    # print(single_food_code_weight.head())

    # weight = single_food_name_weight[single_food_name_weight["ingredient"] == "墨鱼丝"]["weight"]
    # print(weight.values[0])
    # print(type(weight))
    # print(pd.isna(weight))

