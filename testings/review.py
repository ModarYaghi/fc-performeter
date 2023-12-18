import sys
import os

scritp_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(scritp_dir)
sys.path.append(parent_dir)

from testings.json_handler import JSONDataHandler

config_file_path = r"config/transformed_data.json"

config = JSONDataHandler(config_file_path)

# pss = config.get_sheets_names('pss')

# age = config.get_variable_details('age')

# scr = config.get_dataset_variables('Scr')

scr_dataset = config.get_dataset('Scr')

# filtered_vars = scr_dataset.filter_variables(
    # var_type="datetime64[ns]"
# )

# for var in filtered_vars:
    # print(var.name, var.level)

scr_date = [(var.name, var.level) for var in scr_dataset.filter_variables(var_type="datetime64[ns]")]

print(scr_date)

for i in scr_dataset.variables:
    print(i.name, i.type,i.level)