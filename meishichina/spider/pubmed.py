# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/8/9 22:04
# @File    : pubmed.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import csv



if __name__ == '__main__':

    ua = UserAgent(verify_ssl=False)


    url = "https://pubmed.ncbi.nlm.nih.gov/25700523/"


    headers = {
        'User-Agent': ua.random
    }


    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    print(soup)
