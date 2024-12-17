import pandas as pd

data = pd.read_csv("datasets/re_rel_en_ds.csv")
# print(data.info())


# Correlation matrix to find relationships with the target
correlation_matrix = data.corr(method="spearman")
result = correlation_matrix["relative_support2"]  # the best correlation is 0449
# result.to_clipboard()
