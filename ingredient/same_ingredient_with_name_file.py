# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/6 21:29
# @File    : same_ingredient_with_name_file.py
# @Software: PyCharm

import json
import pandas as pd

def open_json_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    data = open_json_file("mstx.json")

    same_ingredient = []

    for i in range(len(data)):
        id = data[i]["id"]
        title = data[i]["title"]
        ingredients = data[i]["ingredients"]
        same_ingredient.append([id, title, ingredients])

    print(same_ingredient[:5])

    df = pd.DataFrame(same_ingredient, columns=['id', 'title', 'ingredients'])

    print(df.head())

    df.to_csv("same_ingredient_with_name.csv", index=False, encoding='utf-8')



