import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle
import datetime

# from path_management import config_file, ps_raw_data, pt_raw_data, processed_data

from path_management import *
from src.config_reader import YAMLConfigReader
from src.dataset import Dataset

from src.xlsx_decryptor import ExcelDecryptor

# --------------------------For Convenient Display----------------------------
pd.set_option("display.float_format", "{:.1f}".format)
# pd.reset_option('display.float_format')

# Display maximum column width:
pd.set_option("display.max_colwidth", None)

# --------------------------Working Period------------------------------------

# ----------------------------------------------------------------------------


config = YAMLConfigReader(config_file)

# Getting the passwords for the file in raw_data directory - xlsx files
pspw = config.get_passwords_by_directory(ps_raw_data)
ptpw = config.get_passwords_by_directory(pt_raw_data)


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
            dataframe.dropna(subset=dataset.bvars, how="all", inplace=True)

        # Insert the new column
        dataframe.insert(0, sp, sp_init)

        # Assuming you need to perform some operations with dataframe here
        # process_dataframe(dataframe)
        dataframes.append(dataframe)

    compiled_dataframe = pd.concat(dataframes, ignore_index=True)

    return compiled_dataframe


def dtype_trans(
    dataframe: pd.DataFrame,
    dataset: Dataset = None,
    config_path: str = None,
    sheet_name: str = None,
):
    if dataset is None:
        dataset = Dataset(config_path, sheet_name)

    if dataset.dvars:
        dataframe[dataset.dvars] = dataframe[dataset.dvars].apply(pd.to_datetime)

    if dataset.ivars:
        dataframe[dataset.ivars] = dataframe[dataset.ivars].astype("Int64")

    return dataframe


def filter_df_by_date(df, date_column_names, threshold, comparison_type="a"):
    # Ensure specific_date is in datetime format
    threshold_date = pd.to_datetime(threshold)

    # Convert date columns to datetime if not already
    # for col in date_column_names:
    #     df[col] = pd.to_datetime(df[col])

    # Apply the filtering condition
    # Apply the filtering condition based on the comparison type
    if comparison_type == "a":
        return df[(df[date_column_names] > threshold_date).any(axis=1)]
    elif comparison_type == "b":
        return df[(df[date_column_names] < threshold_date).any(axis=1)]
    elif comparison_type == "e":
        return df[(df[date_column_names] == threshold_date).any(axis=1)]
    else:
        raise ValueError(
            "Invalid comparison type. Choose 'after', 'before', or 'equal'."
        )


def get_df(source_data_path, sheet_name, config_file_path=config_file, b=False):
    df_dataset = Dataset(config_file_path, sheet_name)
    df = pd.read_csv(source_data_path)
    df = dtype_trans(df, df_dataset)

    if b:
        # Get the basic Dataframe
        bdf = df[df_dataset.bvars]
        bdf = bdf.drop(["firstname", "lastname"], axis=1)
        return bdf

    return df


class DFrame:
    CONFIG = config_file

    def __init__(self, source_data_path, sheet_name):
        self.source_data_path = source_data_path
        self.sheet_name = sheet_name
        self.dataset = Dataset(DFrame.CONFIG, self.sheet_name)

    def type_casting(self, dataframe: pd.DataFrame):
        if self.dataset.dvars:
            dataframe[self.dataset.dvars] = dataframe[self.dataset.dvars].apply(
                pd.to_datetime
            )

        if self.dataset.ivars:
            dataframe[self.dataset.ivars] = dataframe[self.dataset].astype("Int64")

        return dataframe
