"""
Preperation module

This script renames the encoded dataset columns names by the values of name column in codebook.
"""

import pandas as pd

# Set the option to display all columns
pd.set_option("display.max_columns", None)

codebook = pd.read_excel("codebook.xlsx")

rel_cb = codebook[codebook["relevance"] == 1]
rel_questions = rel_cb["question"].tolist()
# print(len(rel_questions))  # 76

df = pd.read_csv("encoded_dataset.csv")
# print(df.head())

rel_df = df[rel_questions]

rename_mapping = dict(zip(rel_cb["question"], rel_cb.iloc[:, 4]))
re_rel_df = rel_df.rename(columns=rename_mapping)  # pyright: ignore

# print(re_rel_df.head())
re_rel_df.to_csv("re_rel_en_ds.csv", index=False)
re_rel_df.to_clipboard(index=False)
