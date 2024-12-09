"""Correlation Analysis"""

import pandas as pd
from correlation_analysis import CorrelationAnalyzer as ca

df = pd.read_csv("encoded_dataset.csv")
# df.to_clipboard()

re_rel_en_ds = pd.read_csv("re_rel_en_ds.csv")

# re_rel_en_ds.to_clipboard()

corr_anal = ca(re_rel_en_ds)
# print(corr_anal.calculate_correlation)
p_values = corr_anal.calculate_p_values()
p_values.to_clipboard()
