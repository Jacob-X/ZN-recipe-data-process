# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/7/7 10:05
# @File    : ingredient_process.py
# @Software: PyCharm

import json
import csv
import re
import math

def save_list_to_csv(data):
    total_items = len(data)
    max_items_per_file = 120000
    num_files = math.ceil(total_items / max_items_per_file)

    for file_index in range(num_files):
        filename = f"unnormal_data_{file_index + 1}.csv"
        start_index = file_index * max_items_per_file
        end_index = (file_index + 1) * max_items_per_file

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for item in data[start_index:end_index]:
                content = []
                write_content = []
                index = item[0]
                detail = item[1].split(':')

                content.append(index)
                content.append(detail[0])
                content.append(detail[1])
                writer.writerow([content])

def contains_digit(s):
    for c in s:
        if c.isdigit():
            return True
    return False

def main_filter(data):
    filter_meal = []

    for i in range(len(data["data"])):
        ingredients_str = data["data"][i]['配料']
        if ingredients_str == None:
            continue
        # print(ingredients_str)
        ingredients_list = ingredients_str.split(', ')
        main_ingredients = ingredients_list[0].split(':')[1]
        if contains_digit(main_ingredients):
            filter_meal.append(data["data"][i])

    return filter_meal



def remove_parentheses(text):
    pattern = r'（[^（）]*）'  # 匹配中文括号及其内部内容的正则表达式
    result = re.sub(pattern, '', text)
    return result


# 454054个没有定量的菜谱
def find_unnormal_data(data):

    unnormal_data = []
    for da in data:
        index = da['index']
        ingredients_list = da['配料'].split(', ')
        for ingredient in ingredients_list:
            ingredient = remove_parentheses(ingredient)
            if "克" not in ingredient and "g" not in ingredient and "G" not in ingredient:
                unnormal_data.append([index,ingredient])
    return unnormal_data

if __name__ == '__main__':
    ingredient_path = "ingredient.json"

    with open(ingredient_path,encoding="utf-8") as json_file:
        data = json.load(json_file)

    # 过滤之后还有，79329条数据
    filter_meal = main_filter(data)

    print(len(filter_meal))

    print(filter_meal[0:5])

    # unnormal_data = find_unnormal_data(filter_meal)
    # # print(unnormal_data[:10])
    #
    # save_list_to_csv(unnormal_data)
    #
    # # print(filter_meal[0])
