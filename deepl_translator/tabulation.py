""""Extract Valuce Counts of Survey Data"""

import pandas as pd
from irm_final_eval_sources import excel_file_path, open_questions_rename_mapping

dataset = pd.read_excel(excel_file_path)
ds_columns = dataset.columns.to_list()
# print(ds_columns)

columns_file = 'columns.txt'

with open(columns_file, 'w') as f:
    for idx, col in enumerate(dataset.columns):
        f.write(f'{idx}. "{col}", \n')
print(f"Columns have been writtn to {columns_file}")

# Note: Can I download the dataset from kobo with labels?

