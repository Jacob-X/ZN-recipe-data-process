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

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }

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
    # for i in range(len(all_type_list)):
    #     if all_type_list[i][1] =="原味":
    #         print(
    #             i
    #         )

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








