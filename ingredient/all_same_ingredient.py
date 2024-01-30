# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/2 14:17
# @File    : all_same_ingredient.py
# @Software: PyCharm

import json
import csv

# Load the data from the json file
with open('ingredient.json',encoding='utf-8') as f:
    data = json.load(f)

# Create a dictionary to store the information, the keys are the food names, and the values are the lists of [index, food, weight]
food_dict = {}

for item in data['data']:
    index = item['index']
    ingredients = item.get('配料')

    if ingredients:  # check if the ingredients value is not None
        ingredients = ingredients.split(', ')  # split the ingredients string into a list of foods and weights
        for ingredient in ingredients:
            # split each ingredient into food and weight
            parts = ingredient.split(': ')
            if len(parts) != 2:
                continue  # skip this ingredient if it does not have a valid format
            food, weight = parts
            if food not in food_dict:
                food_dict[food] = []
            food_dict[food].append([index, food, weight])

# Convert the dictionary to a list of rows that can be written to a CSV file
rows = []
for food, infos in food_dict.items():
    for info in infos:
        rows.append(info)

# Define the CSV file path
csv_file_path = "same_ingredients.csv"

# Write the rows to the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Food', 'Weight'])  # write the header
    writer.writerows(rows)  # write the data rows
