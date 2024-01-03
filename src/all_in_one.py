import numpy as np
import pandas as pd
import os

from src.data_reader import YAMLDataReader
from src.xlsx_decryptor import ExcelDecryptor

# Avoid representing large numbers in scientific form. To reset, use the commented line.
pd.set_option("display.float_format", "{:.1f}".format)
# pd.reset_option('display.float_format')

# Display maximum column width:
pd.set_option("display.max_colwidth", None)

# ----------------------------------------------------------------------------
# config_path = r'../config/config.json'
config_path = r"../config/config.yaml"
raw_data = r"../data/raw/1023"

# config = JSONDataReader(config_path)
config = YAMLDataReader(config_path)

passwords = config.get_excel_passwords_by_directory(raw_data)
