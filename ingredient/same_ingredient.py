# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/6 21:57
# @File    : same_ingredient.py
# @Software: PyCharm


import pandas as pd
import ast


if __name__ == '__main__':

    # 1. 读取原始 CSV 文件
    df = pd.read_csv('same_ingredient_with_name.csv')

    # 2. 初始化列表来存储数据
    processed_data = []

    # 3. 遍历原始数据
    for index, row in df.iterrows():
        try:
            # 解析 ingredients 列的内容
            ingredient_data = ast.literal_eval(row['ingredients'])

            # 遍历每个食材和其对应的重量
            for ingredient, weight in ingredient_data.items():
                if ingredient == '':
                    continue
                processed_data.append([row['id'], row['title'], ingredient, weight])
        except:
            continue

    # 4. 转化为 DataFrame
    columns = ['Id', 'Food Name', 'Ingredient', 'Weight']
    processed_df = pd.DataFrame(processed_data, columns=columns)

    # 5. 根据 Ingredient 列排序，以将具有相同名称的食材放在一起
    processed_df = processed_df.sort_values(by='Ingredient')

    # 6. 保存为新的 CSV 文件
    output_processed_path = 'processed_same_ingredient_data.csv'
    processed_df.to_csv(output_processed_path, index=False)
