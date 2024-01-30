# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/23 21:38
# @File    : food_code_mapping_by_raw_datas.py
# @Software: PyCharm

# 这个是使用动物和植物的原始数据来进行mapping的代码
import pandas as pd
import numpy as np
import re

if __name__ == '__main__':
    plant_info = pd.read_excel("../../NRV/plant.xlsx")
    animal_info = pd.read_excel("../../NRV/animal.xlsx")

    raw_data = pd.read_csv("../split_struct_food_info.csv")

    plant_code = plant_info.iloc[:, 0:2]
    animal_code = animal_info.iloc[:, 0:2]

    code_list = []

    for index,row in plant_code.iterrows():
        food_name = row['Food name']
        print(food_name)
        food_name = food_name.replace("（", "(").replace("）", ")").replace("［", "[").replace("］", "]").replace("，",
                                                                                                              ",").replace(
            "、", ",")
        if "(" in food_name or ")" in food_name:
            pattern1 = r'^(.*?)\('  # 匹配第一个()前的内容
            pattern2 = r'\((.*?)\)'  # 匹配第一个()内的内容
            pattern3 = r'\[(.*)\]'  # 匹配[]内的内容

            # 名称，名称肯定是1个
            match1 = re.findall(pattern1, food_name)
            # 附属信息，可能有多个，没有，1个
            match2 = re.findall(pattern2, food_name)
            # 别名，可能有多个，没有，1个
            match3 = re.findall(pattern3, food_name)

            ingredient_name = match1[0]
            attach_info = []

            # 在当前情况下，attach的信息是一定存在的
            if len(match2[0]) > 1:
                attach_info = match2[0].split(",")
            else:
                attach_info.extend(match2)

            alias = []
            # 别名信息的判断，可能有多个，1个，没有
            if len(match3) > 1:
                alias = match3.split(",")
            elif len(match3) == 1:
                alias.extend(match3)

            all_ingredient_name = []

            names = []
            names.append(ingredient_name)
            names.extend(alias)
            # print(names)

            all_ingredient_name.extend(names)
            for name in names:
                for info in attach_info:
                    all_ingredient_name.append(name + info)
                    all_ingredient_name.append(info + name)

            code_list.append([row['Food code'], row['Food name'], all_ingredient_name])

        # 一定有别名，但是没附加信息的情况
        elif "[" in food_name or "]" in food_name:
            pattern1 = r'^(.*?)\['  # 匹配[]前的内容
            pattern2 = r'\[(.*)\]'  # 匹配[]内的内容
            match1 = re.findall(pattern1, food_name)
            match2 = re.findall(pattern2, food_name)
            ingredient_name = match1[0]

            alias = []
            if len(match2) > 1:
                alias = match2.split(",")
            else:
                alias.extend(match2)

                names = []
                names.append(ingredient_name)
                names.extend(alias)

                code_list.append([row['Food code'], row['Food name'], names])
            # else:
            #     code_list.append([row['Food code'], row['Food name'],ingredient_name])
        # 只有一个名称的情况
        else:
            ingredient_name = food_name
            code_list.append([row['Food code'], row['Food name'], ingredient_name])


    for index,row in animal_code.iterrows():
        food_name = row['Food name']
        print(food_name)
        food_name = food_name.replace("（", "(").replace("）", ")").replace("［", "[").replace("］", "]").replace("，",
                                                                                                              ",").replace(
            "、", ",")
        if "(" in food_name or ")" in food_name:
            pattern1 = r'^(.*?)\('  # 匹配第一个()前的内容
            pattern2 = r'\((.*?)\)'  # 匹配第一个()内的内容
            pattern3 = r'\[(.*)\]'  # 匹配[]内的内容

            # 名称，名称肯定是1个
            match1 = re.findall(pattern1, food_name)
            # 附属信息，可能有多个，没有，1个
            match2 = re.findall(pattern2, food_name)
            # 别名，可能有多个，没有，1个
            match3 = re.findall(pattern3, food_name)

            ingredient_name = match1[0]
            attach_info = []

            # 在当前情况下，attach的信息是一定存在的
            if len(match2[0]) > 1:
                attach_info = match2[0].split(",")
            else:
                attach_info.extend(match2)

            alias = []
            # 别名信息的判断，可能有多个，1个，没有
            if len(match3) > 1:
                alias = match3.split(",")
            elif len(match3) == 1:
                alias.extend(match3)

            all_ingredient_name = []

            names = []
            names.append(ingredient_name)
            names.extend(alias)
            # print(names)

            all_ingredient_name.extend(names)
            for name in names:
                for info in attach_info:
                    all_ingredient_name.append(name + info)
                    all_ingredient_name.append(info + name)

            code_list.append([row['Food code'], row['Food name'], all_ingredient_name])

        # 一定有别名，但是没附加信息的情况
        elif "[" in food_name or "]" in food_name:
            pattern1 = r'^(.*?)\['  # 匹配[]前的内容
            pattern2 = r'\[(.*)\]'  # 匹配[]内的内容
            match1 = re.findall(pattern1, food_name)
            match2 = re.findall(pattern2, food_name)
            ingredient_name = match1[0]

            alias = []
            if len(match2) > 1:
                alias = match2.split(",")
            else:
                alias.extend(match2)

                names = []
                names.append(ingredient_name)
                names.extend(alias)

                code_list.append([row['Food code'], row['Food name'], names])
            # else:
            #     code_list.append([row['Food code'], row['Food name'],ingredient_name])
        # 只有一个名称的情况
        else:
            ingredient_name = food_name
            code_list.append([row['Food code'], row['Food name'], ingredient_name])

    # code_list = pd.DataFrame(code_list,columns=['Food code','Food name','Food name list'])
    # code_list.to_csv("food_code_list_split.csv",index=False,encoding='utf-8')

    raw_data_list = []
    for index,row in raw_data.iterrows():
        raw_data_list.append(row.tolist())

    for row in raw_data_list:
        mapping_flag = False
        ingredient = row[2]
        # 判断条件是：食材名字在code_list中，或者code_list中的名字在食材中，就加上food code
        for code in code_list:
            for code_name in code[2]:
                # if str(ingredient) == str(code_name) or str(code_name) in str(ingredient) or str(ingredient) in str(code_name):
                if str(ingredient) == str(code_name) or str(ingredient) in str(code_name):
                # if str(ingredient) == str(code_name):
                    row.append(code[0])
                    row.append(code_name)
                    mapping_flag = True
                    break
            if mapping_flag:
                break

        if not mapping_flag:
            row.append("nan")
            row.append("nan")

        print(row)

    raw_data_result = pd.DataFrame(raw_data_list,columns=['title','url','ingredient_name','ingredient_quantity','ingredient_unit','Food_name','Food_code'])
    raw_data_result.to_csv("food_code_mapping_result_2.csv",index=False,encoding='utf-8')



        # for code in code_list:
        #     if row['ingredient_name'] == code[1]:
        #         raw_data.loc[index,'Food code'] = code[0]
        #         raw_data.loc[index,'Food name'] = code[1]
        #     else:
        #         raw_data.loc[index,'Food code'] = "nan"
        #         raw_data.loc[index,'Food name'] = "nan"

    # raw_data.to_csv("food_code_mapping.csv",index=False,encoding='utf-8')
