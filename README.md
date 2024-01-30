# 菜谱定量化流程梳理

## 1. 数据爬取

首先爬取某在线菜谱网页的分类页面，将所有有分类标签的菜谱数据进行爬取，将菜谱的第一分类、第二分类、编号、名称和详情页面的 url 都爬取下来，保存在food_label_data.csv 这个文件中

```python 
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/8 14:59
# @File    : recipe_type.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv

if __name__ == '__main__':

    ua = UserAgent(verify_ssl=False)
    url = 'https://home.meishichina.com/recipe-type.html'
    headers = {
        'User-Agent': ua.random
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    # category_box = soup.select('.category_box.mt20')
    category_box = soup.select('.category_sub.clear')

    all_type_list = []
    for category in category_box:
        # 对应当前大标题下面的小标题
        for li in category.ul.find_all('li'):
            all_type_list.append([category.h3.text,li.a.text,li.a['href']])

    print(all_type_list)

    part_type_list = []

    for i in range(238,len(all_type_list)):
        part_type_list.append(all_type_list[i])

    print(part_type_list)


    # for type in all_type_list:
    for type in part_type_list:
        class_name = []

        url = type[2]

        # 一个菜系的大循环，翻页查找
        while url:
            class_name = []
            headers = {
                'User-Agent': ua.random
            }
            time.sleep(5)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

            content_box = soup.select('.ui_newlist_1.get_num')
            next_page = soup.find('a', string='下一页')
            if next_page:
                url = next_page.get('href')
            else:
                url = None

            for li in content_box[0].find_all('li'):
                if 'clear' in li.get('class', []):
                    continue
                else:
                    data_id = li['data-id']
                    herf = li.find("a")['href']
                    title = li.find("a")['title']
                    class_name.append([type[0],type[1],data_id,title,herf])

            # 动态写入一个csv文件
            with open('food_label_data.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(class_name)
```

从互联网上爬取20万条菜谱数据，使用 fake_useragent 模拟虚拟用户访问页面，使用 BeautifulSoup 爬取整个页面信息，然后从整个页面中找到菜谱的具体名称、食材，制作步骤和分类信息，将以上信息保存到 recipe_info_data.csv 这个文件中

```python
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
```

## 2.菜谱数据预处理

### 2.1菜谱数据去重

将爬虫得到的菜谱数据进行去重处理，使用菜谱的具体信息url进行去重

```python
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
```

### 2.2 结构化菜谱数据

对去重的菜谱数据进行结构化处理，将菜谱中的每一种食材数据分离出来，使用re的正则表达式来从大段的文本信息种提取需要的信息，具体的信息包括：菜谱名称，菜谱详细信息url，食材名称，食材重量

```python
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/23 16:10
# @File    : raw_data_process.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re


if __name__ == '__main__':
    new_raw_data = pd.read_csv("drop_duplicates_recipe_info_data.csv")

    # print(raw_data.head())

    food_info = []

    for index,row in new_raw_data.iterrows():

        raw_title = row['title']
        # 匹配title和url
        pattern_1 = re.compile(r"'(.*)'")
        title_match = pattern_1.search(raw_title)
        if title_match:
            title = title_match.group(1).split()[1].strip("'")

        raw_url = row['url']
        url_match = pattern_1.search(raw_url)
        if url_match:
            url = url_match.group(1).split()[1].strip("'")


        lable = row['lable']
        # pic_url = row['pic_url']
        # raw_ingredients_list =  "['ingredients_list', [('自制酸奶配料', '适量'), ('纯牛奶', '1000ml'), ('乳酸菌', '（1克装,可做1L牛奶）'), ('白糖', '100克'), ('酸奶水果拼盘配料', '适量'), ('脐橙', '1个'), ('苹果', '1个'), ('酸奶', '适量')]]","['type_list', [('口味', '酸甜'), ('工艺', '拌'), ('耗时', '数小时'), ('难度', '简单')]]"
        # 匹配食材和类别
        # pattern_2 = r"\['ingredients_list', \[(.*)\]\]"
        pattern_2 = r"'(.*?)'"
        raw_ingredients_list = row['ingredients_list']
        ingredients_list = re.findall(pattern_2, raw_ingredients_list)
        ingredients_list.remove("ingredients_list")
        processed_ingredients_list = []          # ['饺子', '10个', '丝瓜', '1根', '盐', '适量']
        for ingredient in ingredients_list:
            ingredient = ingredient.strip("(").strip("'").strip(")")
            ingredient = ingredient.replace("(", "")
            ingredient = ingredient.replace("'", "")
            ingredient = ingredient.replace(" ", "")
            processed_ingredients_list.append(ingredient)

        ingredient_result = []
        for i in range(0, len(processed_ingredients_list), 2):
            ingredient_result.append(processed_ingredients_list[i:i + 2])

        # 四种类别的数据，暂时没加上
        # raw_type_list = row['type_list']
        # pattern_3 = r"\['type_list', \[(.*)\]\]"
        # processed_type_list = []     #['口味', '原味', '工艺', '煮', '耗时', '十分钟', '难度', '普通']
        # type_list = re.findall(pattern_3, raw_type_list)[0].split(",")
        # for type in type_list:
        #     type = type.strip("(").strip("'").strip(")")
        #     type = type.replace("(", "")
        #     type = type.replace("'", "")
        #     type = type.replace(" ", "")
        #     processed_type_list.append(type)
        #
        # type_result = []
        # for i in range(0, len(processed_type_list), 2):
        #     type_result.append(processed_type_list[i+1])
        #
        # Flavor = type_result[0]
        # Cooking_method = type_result[1]
        # Time_cost = type_result[2]
        # Difficulty = type_result[3]

        print(title,url,ingredient_result)

        for k in range(len(ingredient_result)):
            ingredient_name = ingredient_result[k][0]
            ingredient_weight = ingredient_result[k][1]

            # food_info.append([title,url,ingredient_name,ingredient_weight,Flavor,Cooking_method,Time_cost,Difficulty])

            food_info.append([title, url, ingredient_name, ingredient_weight])

        # recipe_steps = row['recipe_steps']
        # tips = row['tips']
        # kitchenware = row['kitchenware']

        # print(title,url,processed_ingredients_list)

    df_food_info = pd.DataFrame(food_info, columns=['title', 'url', 'ingredient_name', 'ingredient_weight'])
    df_food_info.to_csv("struct_food_info.csv", index=False, encoding='utf-8')
```

2.3 对得到的结构化数据进一步处理，将菜谱中的食材的重量和单位分离出来，得到split_struct_food_info.csv文件，文件中包含：菜谱名称，菜谱详细信息url，食材名称，食材重量，食材重量单位。

```python
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/23 19:23
# @File    : weight_data_split.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re

# def process_unit(x):
#
#     x = str(x)
#     nums = re.findall('\d+', x)
#     ch_nums = re.findall('([一二两三四五六七八九十半]+)', x)
#     unit = re.findall('([勺匙茶匙汤匙ml片斤两杯碗瓶瓣]+)', x)
#     res = 0
#
#     for n in nums:
#         res += int(n)
#     for cn in ch_nums:
#         if len(cn)>1:
#             res += chinese_to_arabic[cn[0]]
#     # for u in units:
#     #     res += unit_to_g[u]
#     return res, unit

def convert_chinese_num(val):
    if isinstance(val, str):
        return chinese_to_arabic.get(val, val)
    return val

    # 转换单位
# def convert_unit(row):
#     if isinstance(row['quantity'], (str, int, float)) and row['unit'] in unit_to_g:
#         try:
#             return int(row['quantity']) * unit_to_g.get(row['unit'], 1)
#         except ValueError:
#             return row['quantity']
#     return row['quantity']



if __name__ == '__main__':

    raw_data = pd.read_csv("struct_food_info.csv")

    # 中文数字到阿拉伯数字的映射
    chinese_to_arabic = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
        '两': 2,
        '半': 0.5,
        '个': 1,
        '只': 1,
        '块': 1,
        '瓣': 1,
        '颗': 1,
        '粒': 1,
        '枚': 1
        # ... 其他数字
    }

    # 单位到g的转换
    unit_to_g = {
        '勺': 5,  # 假设1勺=5g
        '小勺': 5,  # 假设1勺=5g
        '大勺': 15,  # 假设1勺=15g
        "汤勺": 15,  # 假设1勺=15g
        "小匙": 5,  # 假设1勺=5g
        "大匙": 15,  # 假设1勺=15g
        '匙': 5,  # 假设1匙=5g
        '茶匙': 5,  # 假设1匙=5g
        '汤匙': 15,  # 假设1汤匙=15g
        'ml': 1,  # 假设1ml=1g
        '片': 3,  # 假设1片=3g
        '斤': 500,  # 假设1斤=500g
        '两': 50,  # 假设1两=50g
        '杯': 200,  # 假设1杯=200g
        '碗': 300,  # 假设1碗=300g
        '瓶': 500,  # 假设1瓶=500g
        '瓣': 10,  # 假设1瓣=10g
        '小碗': 300,  # 假设1小碗=300g
        # ... 其他单位
    }

    # 把quantity的中文字换成数字
    # raw_data['ingredient_weight'] = raw_data['ingredient_weight'].apply(convert_chinese_num)
    #
    # raw_data.to_csv("num_struct_food_info.csv",index=False)

    split_data =[]
    for index,row in raw_data.iterrows():

        quantity = 0
        unit = ""

        ingredient_weight = row["ingredient_weight"]
        pattern = r'(\d+(\.\d+)?)|([一二两三四五六七八九十百千万半]+)'
        results = re.findall(pattern, ingredient_weight)

        if len(results) != 0:
            for result in results[0]:
                if result != '':
                    quantity = result
                    unit = ingredient_weight.replace(quantity, '')
                    break
        else:
            unit = ingredient_weight

        print(ingredient_weight,quantity,unit)

        split_data.append([row["title"], row["url"], row["ingredient_name"], quantity, unit])

    df_split_data = pd.DataFrame(split_data,columns=["title","url","ingredient_name","quantity","unit"])
    df_split_data.to_csv("split_struct_food_info.csv",index=False)
```

## 3.食材数据比对处理

### 3.1 与食材库原始数据进行比对

将split_struct_food_info.csv的数据与公司食材库（植物和动物的食材库）进行比对，应为菜谱中的食材有各种别名和形容词，在这里的处理过程中，通过正则表达式识别食材的别名和形容词，将食材库中的食材的别名和形容词进行排列组合后，然后与菜谱中的食材进行比对。得到的结果存储到food_code_mapping_result_2.csv中。

```python
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

```

### 3.2 与先前的food_code文件中的食材进行比对

之前有一份匹配好的food_code文件，里面有一部分食材和对应食材标准名称的匹配，在这里，将先前处理过的split_struct_food_info.csv与food_code中食材名称进行比对，然后将比对后的结果。首先对food_code的数据进行去重处理，去重的数据保存到food_code_unique.csv中，然后用去重的数据进行比对。得到的结果存储到food_code_success_mapping.csv文件中

去重处理

```python
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 18:13
# @File    : food_code_extract.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re


if __name__ == '__main__':
    raw_data = pd.read_excel("food_code_1.xlsx")

    food_code = raw_data.drop_duplicates(subset=['ingredient_v'], keep='first')

    food_code = food_code[['ingredient_v','ingredient_vv','food_name','food_code_1']]

    food_code.to_csv("food_code_unique.csv",index=False,encoding='utf-8-sig')

```

食材名称比对

```python 
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/24 18:29
# @File    : food_code_mapping_by_extract_data.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import re


if __name__ == '__main__':

    food_code = pd.read_csv("food_code_unique.csv")
    raw_data = pd.read_csv("../split_struct_food_info.csv")

    food_code_list = []
    for index,row in food_code.iterrows():
        food_code_list.append(row.to_list())

    raw_data_list = []
    for index,row in raw_data.iterrows():
        raw_data_list.append(row.tolist())

    for row in raw_data_list:
        mapping_flag = False
        for code in food_code_list:
            if row[2] == code[0]:
                row.extend(code[1:])
                mapping_flag = True
                break
        if not mapping_flag:
            row.extend(["","",""])

        print(row)

    mapping_data = pd.DataFrame(raw_data_list,columns=['title','url','ingredient_name','quantity','unit','food_name_1',"food_name_2",'food_code'])
    mapping_data.to_csv("food_code_success_mapping.csv",index=False,encoding='utf-8-sig')

```

### 3.3 单位标准化，中文数字转化，食材重量中位数计算

首先使用正则表达式将菜谱数据中的食材的单位和中文数字识别出来，将常见的容器单位转化为标准的重量单位(g)，例如勺，杯，碗等常用的食材单位；将中文的数字转化为英文。最后将转换的结果存储到food_code_standard_weight.csv这个文件中。

对具有相同的名称或food_code的食材，分别计算两个中位数，名称中位数和food_code中位数，用于后面的“适量”食材的定量化处理。

single_food_name_weight_2.csv：名称相同的食材的质量中位数

single_food_code_weight.csv：food_code相同的食材的质量中位数


```python
# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/6 23:01
# @File    : food_code_weight.py
# @Software: PyCharm
from datetime import datetime

import pandas as pd
from datetime import datetime
import re


def process_unit(x):

    x = str(x)
    nums = re.findall('\d+', x)
    ch_nums = re.findall('([一二两三四五六七八九十半]+)', x)
    unit = re.findall('([勺匙茶匙汤匙ml片斤两杯碗瓶瓣]+)', x)
    res = 0

    for n in nums:
        res += int(n)
    for cn in ch_nums:
        if len(cn)>1:
            res += chinese_to_arabic[cn[0]]
    # for u in units:
    #     res += unit_to_g[u]
    return res, unit

def convert_chinese_num(val):
    if isinstance(val, str):
        return chinese_to_arabic.get(val, val)
    return val

    # 转换单位
def convert_unit(row):
    if isinstance(row['quantity'], (str, int, float)) and row['unit'] in unit_to_g:
        try:
            return int(row['quantity']) * unit_to_g.get(row['unit'], 1)
        except ValueError:
            return row['quantity']
    return row['quantity']


if __name__ == '__main__':
    #
    # # Reading the "extended" sheet from the Excel file
    # df = pd.read_excel("food_code_1_sort.xlsx", sheet_name="extended")

    df = pd.read_csv("data/food_code_success_mapping.csv")
    print(df.head())

    # 中文数字到阿拉伯数字的映射
    chinese_to_arabic = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 10,
        '两': 2,
        '半': 0.5,
        '个': 1,
        '只': 1,
        '块': 1,
        '瓣': 1,
        '颗': 1,
        '粒': 1,
        '枚': 1
        # ... 其他数字
    }

    # 单位到g的转换
    unit_to_g = {
        '勺': 5,  # 假设1勺=5g
        '小勺': 5,  # 假设1勺=5g
        '大勺': 15,  # 假设1勺=15g
        "汤勺": 15,  # 假设1勺=15g
        "小匙": 5,  # 假设1勺=5g
        "大匙": 15,  # 假设1勺=15g
        '匙': 5,  # 假设1匙=5g
        '茶匙': 5,  # 假设1匙=5g
        '汤匙': 15,  # 假设1汤匙=15g
        'ml': 1,  # 假设1ml=1g
        '片': 3,  # 假设1片=3g
        '斤': 500,  # 假设1斤=500g
        '两': 50,  # 假设1两=50g
        '杯': 200,  # 假设1杯=200g
        '碗': 300,  # 假设1碗=300g
        '瓶': 500,  # 假设1瓶=500g
        '瓣': 10,  # 假设1瓣=10g
        '小碗': 300,  # 假设1小碗=300g
        # ... 其他单位
    }


    # 把quantity的中文字换成数字
    df['quantity'] = df['quantity'].apply(convert_chinese_num)

    # 把unit的中文字换成数字，提取单位进行转换

    # for index, row in df.iterrows():
    #     quantity, unit = process_unit(str(row['unit']))
    #     if quantity != 0:
    #         print(quantity, unit)
    #         row['quantity'] = quantity
    #         row['unit'] = unit
    #     print(row['quantity'],row['unit'])

    # 转换单位
    df['quantity'] = df.apply(convert_unit, axis=1)
    # 克转换成g
    df['unit'] = df['unit'].apply(lambda x: 'g' if x in unit_to_g else x)

    for index, row in df.iterrows():
        if row["unit"] == "克":
            df.at[index, 'unit'] = 'g'

    df.to_csv('food_code_standard_weight.csv', index=False)

    # # 针对每一个food_code_1，计算一个中位数
    # food_code_list = df["ingredient_name"].unique().tolist()
    #
    # food_code_weight = {}
    #
    # for food_code in food_code_list:
    #     print(food_code)
    #     food_data = df[df["ingredient_name"] == food_code]
    #     food_data = food_data[food_data['unit'] == 'g']
    #     food_data = food_data[food_data['quantity'].apply(type) != datetime]
    #     food_data = food_data[food_data['quantity'].apply(type) != str]
    #     # food_data = food_data[food_data['quantity'].apply(type) == float]
    #
    #     for index, row in food_data.iterrows():
    #         if isinstance(row['quantity'], pd.Timestamp):
    #             food_data.drop(index, inplace=True)
    #     print(food_data.values)
    #
    #     median_weight = food_data[food_data['unit'] == 'g']['quantity'].median()
    #     food_code_weight[food_code] = median_weight
    #
    # print(food_code_weight)
    #
    # df_data = pd.DataFrame(food_code_weight.items(), columns=['ingredient_name', 'weight'])
    # df_data.to_csv("single_food_name_weight_2.csv", index=False)


    # 对于“适量”的处理
    # for index, row in df[df['unit'] == '适量'].iterrows():
    #     median_weight = df[(df['food_code_1'] == row['food_code_1']) & (df['unit'] == 'g') & df['quantity'].apply(
    #         lambda x: isinstance(x, float))]['quantity'].median()
    #     df.at[index, 'quantity'] = median_weight
    #     df.at[index, 'unit'] = 'g'

    # df.to_csv('food_code_weight_1.csv', index=False)

    # print(df.head(20))
```

### 3.4 “适量”食材的处理

food_code_standard_weight.csv是比对过food_code的食材数据，里面包含了：title,url,ingredient_name,quantity,unit,food_name_1,food_name_2,food_code这些数据。对food_code_standard_weight.csv中的食材进行定量化处理，将定量成功的食材保存到success_mapping_result.csv文件中，定量化失败的食材数据保存到"manual.csv"中。

```python
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
```

3.5 食材定量完整检测

对success_mapping_result.csv中的食材数据进行完整性检测，具体来说就是检测一个菜谱中的全部是否全部都已经被定量，将完整定量化的菜谱保存到recipe_integrity_check.csv文件中。

```python
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
```
