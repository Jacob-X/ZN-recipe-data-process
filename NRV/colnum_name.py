# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/9/11 17:00
# @File    : colnum_name.py
# @Software: PyCharm

import pandas as pd

if __name__ == '__main__':
    animal = pd.read_excel("animal.xlsx")

    plant = pd.read_excel("plant.xlsx")


    animal_col = animal.columns.tolist()

    print(len(animal_col))
    print(animal_col)

    print("=====================================")
    #
    plant_col = plant.columns.tolist()

    print(plant_col)
    print(len(plant_col))