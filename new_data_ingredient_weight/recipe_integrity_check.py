# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 22:04
# @File    : recipe_integrity_check.py
# @Software: PyCharm
import pandas as pd
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    mapping_result = pd.read_csv("success_mapping_result.csv")
    raw_data = pd.read_csv("../raw_data_process/struct_food_info.csv")

    print(len(mapping_result))
    print(len(raw_data))

    mapping_result_url_counts = mapping_result['url'].value_counts()
    raw_data_url_counts = raw_data['url'].value_counts()


    df_mapping_result = pd.DataFrame(mapping_result_url_counts, columns=['url', 'counts'])
    df_raw_data = pd.DataFrame(raw_data_url_counts, columns=['url', 'counts'])

    # 比较两个url的数量是否一致
    mapping_result_list = []
    for index,row in df_mapping_result.iterrows():
        mapping_result_list.append([index,row['url']])

    raw_data_list = []
    for index,row in df_raw_data.iterrows():
        raw_data_list.append(([index,row['url']]))

    recipe_list = []

    for result in tqdm(mapping_result_list):
        for rdata in raw_data_list:
            if result[0] == rdata[0]:
                if result[1] == rdata[1]:
                    recipe_list.append(result[0])
                    continue


    df_result = pd.DataFrame(recipe_list,columns=['url'])
    df_result.to_csv("recipe_integrity_check.csv",index=False)
