# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/23 16:10
# @File    : raw_data_process.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import re


if __name__ == '__main__':
    # "['title', '茄汁土豆牛腩']",
    # "['url', 'https://home.meishichina.com/recipe-649954.html']",
    # "['lable', ['热菜', '家常菜']]",
    # "['pic_url', 'https://i3.meishichina.com/atta/recipe/2023/05/17/2023051716843296632672578010238.JPG?x-oss-process=style/p800']",
    # "['ingredients_list', [('牛腩', '适量'), ('土豆', '适量'), ('葱花', '适量'), ('花生油', '适量'), ('盐', '适量'), ('蚝油', '适量'), ('生抽', '适量'), ('海底捞番茄底料', '适量')]]",
    # "['type_list', [('口味', '原味'), ('工艺', '焖'), ('耗时', '一小时'), ('难度', '简单')]]",
    # "['recipe_steps', [('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843357770883218010238.JPG?x-oss-process=style/p320', '1海底捞番茄底料备用。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843357795901518010238.JPG?x-oss-process=style/p320', '2牛腩洗净切块。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843357878136758010238.JPG?x-oss-process=style/p320', '3牛腩冷水下锅焯烫出血水后洗净。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843357933577748010238.JPG?x-oss-process=style/p320', '4锅中热油，放入牛腩翻炒。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358420774418010238.JPG?x-oss-process=style/p320', '5加入适量蚝油，生抽。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358467233078010238.JPG?x-oss-process=style/p320', '6翻炒均匀入味。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358536104018010238.JPG?x-oss-process=style/p320', '7放入番茄底料炒匀。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358616494628010238.JPG?x-oss-process=style/p320', '8加入适量清水。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358677585908010238.JPG?x-oss-process=style/p320', '9将牛腩转入高压锅。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358733012748010238.JPG?x-oss-process=style/p320', '10大火煮开转中小火压20分钟左右。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358789952088010238.JPG?x-oss-process=style/p320', '11压好的牛腩开盖。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358849784268010238.JPG?x-oss-process=style/p320', '12土豆去皮洗净切小块。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358923265948010238.JPG?x-oss-process=style/p320', '13将土豆放入牛腩中。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843358996012088010238.JPG?x-oss-process=style/p320', '14大火煮开转中小火，焖至土豆粉糯，出锅前再试味加少许盐调味。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843359051265238010238.JPG?x-oss-process=style/p320', '15成品。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843359122483818010238.JPG?x-oss-process=style/p320', '16成品。'), ('https://i3.meishichina.com/atta/step/2023/05/17/2023051716843359181625148010238.JPG?x-oss-process=style/p320', '17成品。')]]",
    # "['Tips', '\t\t\t\t\t来自 美食天下 _蒍鉨变乖々 的作品\n\t\t\t\t']",
    # "['厨具', '使用的厨具：高压锅']"

    # title,url,lable,pic_url,ingredients_list,type_list,recipe_steps,tips,kitchenware

    # raw_data = pd.read_csv("../meishichina/food_info/recipe_info_data.csv")
    # # 对数据进行去重，按url去重
    # raw_data = raw_data.drop_duplicates(subset=['url'], keep='first')
    # print(len(raw_data))
    # raw_data.to_csv("drop_duplicates_recipe_info_data.csv", index=False, encoding='utf-8')


    new_raw_data = pd.read_csv("drop_duplicates_recipe_info_data.csv")

    # print(raw_data.head())
    #

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


        # "['title', '自制酸奶与酸奶水果拼盘']",
        # "['url', 'https://home.meishichina.com/recipe-101950.html']",
        # "['lable', ['饮品', '自制食材', '冰品']]",
        # "['pic_url', 'https://i3.meishichina.com/atta/recipe/2012/11/26/20121126133705170350295.jpg?x-oss-process=style/p800']",
        # "['recipe_steps', [('https://i3.meishichina.com/atta/step/201211/201211261346111354875447.JPG?x-oss-process=style/p320', '1原料图'), ('https://i3.meishichina.com/atta/step/201211/201211261346081354337737.JPG?x-oss-process=style/p320', '2将少量牛奶倒入奶锅，加入白糖小火煮溶，牛奶不用完全煮开，60度左右即可；'), ('https://i3.meishichina.com/atta/step/201211/201211261346101354226295.JPG?x-oss-process=style/p320', '3煮好的牛奶晾凉后，加入乳酸菌并搅拌至溶解；'), ('https://i3.meishichina.com/atta/step/201211/201211261346541354242311.JPG?x-oss-process=style/p320', '4再将余下的牛奶倒入，混合均匀；'), ('https://i3.meishichina.com/atta/step/201211/201211261347071354651586.JPG?x-oss-process=style/p320', '5将牛奶倒入消毒过的酸奶钢盘里；'), ('https://i3.meishichina.com/atta/step/201211/201211261347271354074211.JPG?x-oss-process=style/p320', '6盖好钢盘的内盖'), ('https://i3.meishichina.com/atta/step/201211/201211261347451354794218.JPG?x-oss-process=style/p320', '7再盖好外盖；'), ('https://i3.meishichina.com/atta/step/201211/201211261348131354743665.JPG?x-oss-process=style/p320', '8接通电源，按定时键，时间设定为8-12小时，我设了8小时；'), ('https://i3.meishichina.com/atta/step/201211/201211261348411354765183.JPG?x-oss-process=style/p320', '98小时后，牛奶便发酵凝固成酸奶了，可以直接吃，也可以冷藏后再吃。'), ('https://i3.meishichina.com/atta/step/201211/201211261349111354630944.JPG?x-oss-process=style/p320', '10自制酸奶很好喝'), ('https://i3.meishichina.com/atta/step/201211/201211261350021354321304.JPG?x-oss-process=style/p320', '11酸奶水果拼盘的原料图（脐橙1个、苹果1个、酸奶适量）'), ('https://i3.meishichina.com/atta/step/201211/201211261352501354449870.JPG?x-oss-process=style/p320', '12苹果去皮切块，置入淡盐水中（凉开水加适量盐融化成淡盐水），以防表面被氧化变黑；'), ('https://i3.meishichina.com/atta/step/201211/201211261352231354425930.JPG?x-oss-process=style/p320', '13橙子去皮，取下果肉；'), ('https://i3.meishichina.com/atta/step/201211/201211261352241354105386.JPG?x-oss-process=style/p320', '14将苹果取出滤去水份，并与橙子摆盘'), ('https://i3.meishichina.com/atta/step/201211/201211261352191354730474.JPG?x-oss-process=style/p320', '15淋上酸奶，即成酸奶水果拼沙拉，开始享用吧。')]]","['Tips', '\t\t\t\t\t1、酸奶机里的钢盘，第一次使用次，要洗干净，用开水烫过消毒，晾干水，再进行做酸奶，做酸奶的所有容器不能沾有水与油，否则酸奶会坏掉。\r\n2、如果没有乳酸菌，可以用市售酸奶作为发酵剂。\r\n3、做酸奶时可随自己喜好添加糖或不加糖，我个人觉得没加糖做的酸奶比较酸，尽管吃时可以加糖和蜂蜜，但没有加了糖做出来的好吃。\r\n4、不要空腹喝酸奶，因空腹时饮用酸奶，乳酸菌易被杀死，保健作用减弱。\r\n5、饮用时，最好不要加热，因酸奶中的有效益生菌在加热后会大量死亡，营养价值降低，味道也会有所改变。\r\n6、一次做的酸奶不要太多，能够供你喝两天为宜，约500毫升，做多了放置的时间过长，酸奶会变得太酸，不好喝了。 \n\t\t\t\t']",
        # "['厨具', '使用的厨具：酸奶机、煮锅']"

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