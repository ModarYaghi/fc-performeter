"""
Preperation module
"""

import pandas as pd


codebook = pd.read_excel("codebook.xlsx")

rel_cb = codebook[codebook["relevance"] == 1]
rel_columns = rel_cb["question"]
rel_col_list = rel_columns.tolist()
# print(rel_columns)

df = pd.read_csv("encoded_dataset.csv")

rel_df = df[rel_col_list]
# print(rel_df.shape)

for col in rel_df.columns:
    for value in rel_columns:
        