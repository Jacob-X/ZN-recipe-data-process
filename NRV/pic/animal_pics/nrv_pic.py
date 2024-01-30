# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/7/26 9:36
# @File    : nrv_pic.py
# @Software: PyCharm
import pandas as pd

import matplotlib.pyplot as plt
import six
import numpy as np


def render_mpl_table(data,table_title, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
            cell.set_text_props(ha='center', va='center')
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])
            cell.set_text_props(ha='center', va='center')

    if table_title:
        ax.set_title(table_title, fontsize=22, fontweight='bold', loc='center', pad=20)


    return ax
# Load the new Excel file
df_new_single_row = pd.read_excel("../animal_nrv_analysis.xlsx")

for i in range(457,len(df_new_single_row)):
# for i in range(2):

    new_single_row = df_new_single_row.iloc[i]
    print(new_single_row)

    nrv_name = ['Energy kJ', 'Protein', 'Fat', 'Carbohydrate', 'Vitamin A', 'Thiamin',
                'Riboflavin', 'Niacin', 'Vitamin B6', 'Folate', 'Vitamin B12',
                 'Vitamin C','Vitamin D', 'Vitamin K', 'Calcium', 'Phosphorus',
                'Potassium', 'Sodium', 'Iron', 'Zinc', 'Selenium', 'Copper', 'Iodine']

    nrv_weight = ["千焦","克","克","克","微克","毫克",
                  "毫克","毫克","毫克","微克","微克",
                  "毫克","微克","微克","毫克","毫克",
                  "毫克","毫克","毫克","毫克","微克","毫克","微克"]


    nrv_value =['Energy kJ NRV%', 'Protein NRV%', 'Fat NRV%', 'Carbohydrate NRV%','Vitamin A NRV%','Thiamin NRV%',
                'Riboflavin NRV%','Niacin NRV%','Vitamin B6 NRV%', 'Folate NRV%','Vitamin B12 NRV%',
                'Vitamin C NRV%', 'Vitamin D NRV%', 'Vitamin K NRV%','Calcium NRV%','Phosphorus NRV%',
                'Potassium NRV%', 'Sodium NRV%', 'Iron NRV%','Zinc NRV%','Selenium NRV%', 'Copper NRV%','Iodine NRV%']

    # nrv_cn_name = ['能量（千卡）', '蛋白质', '脂肪', '碳水化合物', '维生素A', '硫胺素（维生素B1）',
    #                '核黄素（维生素B2）', '烟酸（维生素B3）', '维生素B6', '叶酸（维生素B9）', '维生素B12',
    #                '维生素C', '维生素D', '维生素K', '钙', '磷','钾', '钠', '铁', '锌', '硒', '铜', '碘']

    nrv_cn_name = ['能量（千卡）', '蛋白质', '脂肪', '碳水化合物', '维生素A', '维生素B1',
                   '维生素B2', '烟酸', '维生素B6', '叶酸', '维生素B12',
                   '维生素C', '维生素D', '维生素K', '钙', '磷',
                   '钾', '钠', '铁', '锌', '硒', '铜', '碘']

    dict_nrv_name = dict(zip(nrv_name, nrv_cn_name))
    dict_nrv_weight = dict(zip(nrv_name, nrv_weight))

    # Create a dictionary with the new row

    nrv_dict ={}
    colnums = df_new_single_row.columns.tolist()

    for col in df_new_single_row.columns:
        if col in nrv_name:
            if str(new_single_row[col]) == "nan":
                new_single_row[col] = 0.0
            if str(new_single_row[col + ' NRV%']) == "nan":
                new_single_row[col + ' NRV%'] = "0.0%"
            nrv_dict[dict_nrv_name[col]] = [str(new_single_row[col])+" "+dict_nrv_weight[col].strip(), new_single_row[col + ' NRV%']]

    new_single_row_df = pd.DataFrame.from_dict(nrv_dict, orient='index').reset_index()

    new_single_row_df.columns = ["Nutrient", "Value/100g", "NRV%"]

    table_names = new_single_row["Food name"]+"营养标签"

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
    render_mpl_table(new_single_row_df, header_columns=0, col_width=4.0,table_title=table_names)
    plt.savefig(str(new_single_row["Food code"])+str(new_single_row["Food name"]).replace("/","、")+"营养标签"+'.png')  # 指定保存的文件名和格式
