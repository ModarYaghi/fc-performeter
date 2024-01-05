import sys
# import numpy as np
import pandas as pd

# import os

# config_path = r'../config/config.json'
config_path = r"C:/Users/myagh/fc-performeter/config/config.yaml"
raw_data = r"C:/Users/myagh/fc-performeter/data/raw/1223/"
processed_data = r"C:/Users/myagh/fc-performeter/data/processed/1223/"

sys.path.append((config_path, raw_data))

from src.data_reader import YAMLDataReader

from src.xlsx_decryptor import ExcelDecryptor

from src.dataset import Dataset

# Avoid representing large numbers in scientific form. To reset, use the commented line.
pd.set_option("display.float_format", "{:.1f}".format)
# pd.reset_option('display.float_format')

# Display maximum column width:
pd.set_option("display.max_colwidth", None)

# ----------------------------------------------------------------------------


# config = JSONDataReader(config_path)
config = YAMLDataReader(config_path)

passwords = config.get_passwords_by_directory(raw_data)
files = [ds['file'] for ds in config.data_source if ds['service'] in ['pss', 'pt']]
psspt_sheets = [
    sheet for service, sheets in config.sheets.items() for sheet_name, sheet in sheets.items()
]

pss_files = [
    'tt_psc_IJ_v04.xlsx',
    'tt_psc_LA_v04.xlsx',
    'tt_psc_MT_v04.xlsx',
    'tt_psc_SA_v04.xlsx',
    'tt_psc_YQ-v04.xlsx'
]
pt_files = [
    'tt_pt_HJ_v04.1.xlsx',
    'tt_pt_HR_v04.1.xlsx',
    'tt_pt_ZN_v04.1.xlsx'
]

pss_sheets = [
    'Scr',
    'Int',
    'GC',
    'IC',
    'FUA',
    'PEI',
    'TRW',
    'TD',
    'CWS',
    'AWS',
]

pt_sheets = [
    'PSFS',
    'PT Int',
    'GPT',
    'IPT',
    'FUP',
]


def compiler(sheet_name, files_list, path_to_config, tracking_tools):
    dataframes = []
    # for sheet in sheets_list:
    sp = (sheet_name + "sp").lower().replace(" ", "")
    dataset = Dataset(path_to_config, sheet_name)

    for file in files_list:
        sp_init = file[7:9]
        dataframe = tracking_tools[file][sheet_name]

        # Simplify the column setting and dropping the first row
        dataframe.columns = dataset.vars
        dataframe = dataframe.iloc[1:].reset_index(drop=True)

        # Improved dropna to handle the case where dataset.bvars is empty or None
        if dataset.bvars:
            dataframe.dropna(subset=dataset.bvars, how='all', inplace=True)

        # Insert the new column
        dataframe.insert(0, sp, sp_init)

        # Assuming you need to perform some operations with dataframe here
        # process_dataframe(dataframe)
        dataframes.append(dataframe)

        compiled_dataframe = pd.concat(dataframes, ignore_index=True)



    return compiled_dataframe
