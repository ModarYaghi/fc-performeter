from enum import Enum, auto
from typing import List, Union

import pandas as pd

from path_management import *
from dataset import Dataset
from xlsx_decryptor import ExcelDecryptor
import warnings

# --------------------------For Convenient Display----------------------------
pd.set_option("display.float_format", "{:.1f}".format)
# pd.reset_option('display.float_format')

# Display maximum column width:
pd.set_option("display.max_colwidth", None)

# Suppress SettingWithCopyWarning
pd.options.mode.chained_assignment = None

# Suppress openpyxl warning about unsupported Data Validation in Excel file
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def compiler(sheet_name, files_list, path_to_config, tracking_tools, ser):
    print(f"Compiler called with sheet_name: {sheet_name}")

    dataframes = []
    # for sheet in sheets_list:
    sp = (sheet_name + "sp").lower().replace(" ", "")
    dataset = Dataset(path_to_config, sheet_name)

    for file in files_list:
        if ser == "pss":
            sp_init = file[7:9]
        elif ser == "pt":
            sp_init = file[6:8]
        else:
            return "sp_init is not valid"
        print(f"Processing file: {file}")
        print(f"Available sheets in this file: {list(tracking_tools[file].keys())}")

        try:
            dataframe = tracking_tools[file][sheet_name]
            print(f"Successfully accessed sheet: {sheet_name}")
        except KeyError as e:
            print(f"KeyError occurred: {e}")
            print(f"Sheet {sheet_name} not found in file {file}")
            continue
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


class FilterType(Enum):
    BF = auto()
    AF = auto()
    IN = auto()
    ON = auto()


def filter_dataframe_on_date(
    df: pd.DataFrame,
    date_columns: Union[str, List[str]],
    date1: Union[str, pd.Timestamp],
    date2: Union[str, pd.Timestamp] = None,
    filter_type: FilterType = FilterType.IN,
) -> pd.DataFrame:
    """
    Filters the DataFrame based on the date conditions provided.
    Uses an Enum for filter types to improve code reliability and maintainability.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    date_columns (Union[str, List[str]]): The column(s) to apply the filter on.
    date1 (Union[str, pd.Timestamp], optional): The primary date to filter against.
    date2 (Union[str, pd.Timestamp], optional): The secondary date to filter against (used for 'between' type).
    filter_type (FilterType): Type of filter to apply.

    Returns:
    pd.DataFrame: The filtered DataFrame.
    """

    if isinstance(date_columns, str):
        date_columns = [date_columns]  # Convert to list if only one column provided

    if filter_type == FilterType.BF:
        condition = (df[date_columns] <= date1).any(axis=1)
    elif filter_type == FilterType.AF:
        condition = (df[date_columns] >= date1).any(axis=1)
    elif filter_type == FilterType.ON:
        condition = (df[date_columns] == date1).any(axis=1)
    elif filter_type == FilterType.IN:
        if date2 is None:
            raise ValueError("date2 must be provided for 'between' filter type.")
        condition = ((df[date_columns] >= date1) & (df[date_columns] <= date2)).any(
            axis=1
        )
    else:
        raise ValueError(
            "Invalid filter_type. Use 'before', 'after', 'equal', or 'between'."
        )

    filtered_df = df[condition]
    return filtered_df


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


def categorize_and_count_ages(ages, start=18, end=80, interval=10):
    """
    Categorize ages into bins and count the number of occurrences in each bin.

    Parameters:
        :param ages: List of ages to categorize.
        :param start: Starting age for the first bin.
        :param end: Ending age for the last bin.
        :param interval: Interval for each age bin.

    Returns:
        pd.Series: Counts of ages in each bin.

    """
    # Define the age bins
    bins = list(range(start, end + 1, interval))

    # Define the labels for each bin
    labels = [f"{bins[i]}-{bins[i + 1] - 1}" for i in range(len(bins) - 1)]

    # Create a pandas' series for the ages
    age_series = pd.Series(ages)

    # Create a new series for the age bins
    age_groups = pd.cut(age_series, bins=bins, labels=labels, right=False)

    # Count the number of occurrences in each bin
    age_counts = age_groups.value_counts(sort=True)
    age_counts = age_counts.sort_index(na_position="first")

    # return age_counts
    return age_counts


if __name__ == "__main__":
    pass
