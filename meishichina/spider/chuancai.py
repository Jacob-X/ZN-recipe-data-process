# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/2 11:12
# @File    : chuancai.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = "https://home.meishichina.com/recipe/chuancai/page/8/"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    recipes = []

    for li in soup.find_all('li', attrs={'data-id': True}):
        recipe = {}
        recipe['id'] = li['data-id']
        pic_div = li.find('div', class_='pic')
        recipe['link'] = pic_div.find('a')['href']
        recipe['title'] = pic_div.find('a')['title']
        recipe['image'] = pic_div.find('img')['data-src']
        detail_div = li.find('div', class_='detail')
        recipe['author'] = detail_div.find('a').text
        recipe['ingredients'] = detail_div.find('p', class_='subcontent').text
        recipes.append(recipe)

    print(len(recipes))

    for recipe in recipes:
        print(recipe)

