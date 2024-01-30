# -*- coding: utf-8 -*-
# @Author  : jacob xu
# @Time    : 2023/7/25 22:56
# @File    : NRV_compute.py
# @Software: PyCharm


import pandas as pd

# Load the Excel file
df = pd.read_excel("animal.xlsx")

# Define the list of NRV-related columns
nrv_cols = [
    "Food code", "Food name", "Food group", "Sub group",
    "Energy kcal", "Energy kJ", "Protein", "Fat", "Carbohydrate",
    "Fiber", "Sodium", "Vitamin A", "Vitamin D", "Vitamin E",
    "Vitamin K", "Vitamin C", "Thiamin", "Riboflavin", "Niacin",
    "Vitamin B6", "Folate", "Vitamin B12", "Calcium", "Phosphorus",
    "Potassium", "Iron", "Zinc", "Copper", "Iodine", "Selenium", "Molybdenum"
]

# Extract the NRV-related columns
nrv_df = df.loc[:, df.columns.isin(nrv_cols)]

# Define the new daily recommended intake for each nutrient
new_nrv_values = {
    "Energy kcal": 8400*0.239,  # Convert from kJ to kcal
    "Protein": 60,
    "Fat": 60,
    "Saturated Fat": 20,
    "Carbohydrate": 300,
    "Dietary Fiber": 25,
    "Vitamin A": 800,  # Convert from μg to mg
    "Vitamin D": 10,
    "Vitamin E": 14,
    "Vitamin K": 80,
    "Thiamin": 1.4,
    "Riboflavin": 1.4, # Vitamin B2
    "Vitamin B6": 1.4,
    "Vitamin B12": 2.4,
    "Vitamin C": 100,
    "Niacin": 14,
    "Folate": 350,
    "Pantothenic Acid": 5,
    "Biotin": 30,
    "Choline": 500,
    "Calcium": 800,
    "Phosphorus": 700,
    "Potassium": 2000,
    "Sodium": 2000,
    "Magnesium": 300,
    "Iron": 15,
    "Zinc": 11,
    "Iodine": 120,
    "Selenium": 60,
    "Copper": 0.8,
    "Fluoride": 1,
    "Manganese": 3
}

# Calculate the NRV percentage for each nutrient in each food using the new NRV values
for nutrient, nrv in new_nrv_values.items():
    if nutrient in nrv_df.columns:
        # Convert the nutrient values to numeric (ignore errors for non-numeric values)
        nrv_df[nutrient] = pd.to_numeric(nrv_df[nutrient], errors="coerce")

        # Calculate the NRV percentage
        nrv_df[nutrient + "_NRV"] = (nrv_df[nutrient] / nrv) * 100

# Round all the numeric columns to 1 decimal place
nrv_df = nrv_df.round(decimals=1)

# Convert the NRV percentages to percentage format
percentage_cols = [col for col in nrv_df.columns if "NRV%" in col]
for col in percentage_cols:
    # nrv_df[col] = nrv_df[col].apply(lambda x: str(x) + '%' if pd.notnull(x) else '')
    nrv_df[col] = nrv_df[col].apply(lambda x: str(x) if pd.notnull(x) else '')

# Save the final DataFrame to an Excel file
nrv_df.to_excel("animal_nrv_analysis.xlsx", index=False)



