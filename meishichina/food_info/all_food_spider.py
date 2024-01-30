# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/15 15:43
# @File    : all_food_spider.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv
import pandas as pd



if __name__ == '__main__':

    all_food = pd.read_csv("food_label_data.csv")

    for index,row in all_food.iterrows():
        # print(row["url"])
        # 151145
        if index > 204029:
            recipe_info = []
            ua = UserAgent(verify_ssl=False)

            # url = "https://home.meishichina.com/recipe-579489.html"
            # url = "https://home.meishichina.com/recipe-512023.html"
            url = row["url"]
            time.sleep(2)

            headers = {'User-Agent': ua.random}

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

            # 菜谱的标题和链接
            if soup.find('a', id='recipe_title') is None:
                continue

            title = soup.find('a', id='recipe_title').text.strip()
            url = soup.find('a', id='recipe_title')['href']

            if title is not None:
                recipe_info.append(["title",title])
            else:
                recipe_info.append(["title",""])

            if url is not None:
                recipe_info.append(["url",url])
            else:
                recipe_info.append(["url",""])

            # 菜谱的标签
            lable = []
            path_lable = soup.find('div', id='path')

            for a in path_lable.find_all('a',target = "_blank"):
                lable.append(a.text.strip())

            recipe_info.append(["lable",lable])

            # 菜谱的主图
            detial = soup.find('div', class_='recipDetail')
            pic_url = detial.find('a',class_="J_photo").find('img')['src']
            recipe_info.append(["pic_url",pic_url])

            field_list = soup.find_all("fieldset",class_="particulars")

            # 食材的名称和用量
            ingredients_name = []
            ingredients_value = []
            for field in field_list:
                for li in field.find_all('li'):
                    for s1 in li.find_all('span',class_='category_s1'):
                        ingredients_name.append(s1.text.strip())
                    for s2 in li.find_all('span',class_='category_s2'):
                        ingredients_value.append(s2.text.strip())

            ingredients_list = zip(ingredients_name,ingredients_value)
            # print(list(ingredients_list))

            recipe_info.append(["ingredients_list",list(ingredients_list)])

            # 菜谱的口味，工艺等种类数据
            type_value = []
            type_name = []
            type_col = soup.find('div',class_='recipeCategory_sub_R mt30 clear')
            for li in type_col.find_all('li'):
                for s1 in li.find_all('span', class_='category_s1'):
                    if s1.text.strip() is not None:
                        type_value.append(s1.text.strip())
                    else:
                        type_value.append("")
                for s2 in li.find_all('span', class_='category_s2'):
                    if s2.text.strip() is not None:
                        type_name.append(s2.text.strip())
                    else:
                        type_name.append("")
            type_list = zip(type_name,type_value)
            # print(list(type_list))
            recipe_info.append(["type_list",list(type_list)])

            # 菜谱的步骤
            recipe_imgs = []
            recipe_words = []
            recipeStep = soup.find('div',class_='recipeStep')

            for li in recipeStep.find_all('li'):
                for imgs in li.find_all('div',class_='recipeStep_img'):
                    if imgs.find('img'):
                        recipe_imgs.append(imgs.find('img')['src'])
                    else:
                        recipe_imgs.append("")
                for words in li.find_all('div',class_='recipeStep_word'):
                    if words.text.strip() is not None:
                        recipe_words.append(words.text.strip())
                    else:
                        recipe_words.append("")

            recipe_steps = zip(recipe_imgs,recipe_words)
            # print(list(recipe_steps))
            recipe_info.append(["recipe_steps",list(recipe_steps)])

            # 菜谱的小贴士
            tips = soup.find('div',class_='recipeTip').text.strip("\n")
            # print(tips)
            recipe_info.append(["Tips",tips])

            # 菜谱的厨具
            kitchenware = ""
            tip_text = soup.find_all('div',class_='recipeTip mt16')
            for tip in tip_text:
                info = tip.text.strip()
                if "厨具" in info:
                    kitchenware = info
            recipe_info.append(["厨具",kitchenware])

            with open('recipe_info_data.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(recipe_info)




