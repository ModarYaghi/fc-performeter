import os
import pandas as pd
import pprint
from tabulate import tabulate
from all_in_one import (
    processed_data,
    Dataset,
    dtype_trans,
    config_file,
    filter_df_by_date,
)
from IPython.display import display, HTML

pd.set_option("display.max_columns", 5)
pd.set_option("display.max_rows", 100)
pd.set_option("display.width", 1000)

path = os.path.join(processed_data, "scr_1223.csv")
sheet_name = "Scr"
df_dataset = Dataset(config_file, sheet_name)
scr = pd.read_csv(path)
scr = dtype_trans(scr, df_dataset)

threshold = "2023-09-30"
scr_q4 = filter_df_by_date(scr, df_dataset.dvars, threshold)

output = scr_q4
