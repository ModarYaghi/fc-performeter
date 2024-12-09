"""
Preperation module
"""

import pandas as pd

codebook = pd.read_excel("codebook.xlsx")

rel_cb = codebook[codebook["relevance"] == 1]
rel_questions = rel_cb["question"].tolist()
# print(len(rel_questions))  # 76

df = pd.read_csv("encoded_dataset.csv")

rel_df = df[rel_questions]

rename_mapping = dict(zip(rel_cb["question"], rel_cb.iloc[:, 4]))
re_rel_df = rel_df.rename(columns=rename_mapping)  # pyright: ignore

# print(re_rel_df.head())
re_rel_df.to_csv("re_rel_en_ds.csv", index=False)
