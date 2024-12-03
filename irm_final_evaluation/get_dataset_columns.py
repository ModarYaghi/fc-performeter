"""
Preperation module
"""

import numpy as np
import pandas as pd

codebook = pd.read_excel("codebook.xlsx")

rel_cb = codebook[codebook["relevance"] == 1]
rel_columns = rel_cb["question"]
rel_col_list = rel_columns.tolist()
# print(rel_columns)

df = pd.read_csv("encoded_dataset.csv")

rel_df = df[rel_col_list]

for value in rel_columns:  # This is columns names in cb
    index = np.where(rel_cb == value)
    row_ind, col_ind = index[0][0], index[1][0]
    value_at_index = rel_cb.iloc[(row_ind, col_ind)]
    # for col in rel_df.columns.tolist():  # This the question in df
    # df_value = rel_df.columns.tolist()[row_ind]
    col_inc = col_ind
    # print(col_inc)
    # FIX: rel_cb dataset columns are the rel_cb column index 1.
    # FIX: The following line indices should be reversed,
    # FIX: but I need to find how to find the rwo index.
    target_value = rel_cb.iloc[(row_ind, col_inc)]
    print(target_value)
    col_inc += 1
