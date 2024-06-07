import pandas as pd
from typing import Union, List
from enum import Enum, auto
from path_management import *
from src.dataset import Dataset

from src.xlsx_decryptor import ExcelDecryptor

# --------------------------For Convenient Display----------------------------
pd.set_option("display.float_format", "{:.1f}".format)
# pd.reset_option('display.float_format')

# Display maximum column width:
pd.set_option("display.max_colwidth", None)


# --------------------------Working Period------------------------------------
start = '2024-03-01'
end = '2024-05-31'
# ----------------------------------------------------------------------------


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


class FilterType(Enum):
    BF = auto()
    AF = auto()
    IN = auto()
    ON = auto()


def filter_dataframe_on_date(df: pd.DataFrame, date_columns: Union[str, List[str]],
                             date1: Union[str, pd.Timestamp], date2: Union[str, pd.Timestamp] = None,
                             filter_type: FilterType = FilterType.IN) -> pd.DataFrame:
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
        condition = ((df[date_columns] >= date1) & (df[date_columns] <= date2)).any(axis=1)
    else:
        raise ValueError("Invalid filter_type. Use 'before', 'after', 'equal', or 'between'.")

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


if __name__ == '__main__':
    pass
