import pandas as pd
from typing import List, Dict, Any, Union
from datetime import datetime

class DatasetManager:
    """
    A class to manage multiple related datasets, providing flexible querying and manipulation capabilities.
    """

    def __init__(self, file_paths: Dict[str, str]):
        """
        Initialize the DatasetManager with a dictionary of dataset names and file paths.

        Args:
            file_paths (Dict[str, str]): A dictionary where keys are dataset names and values are file paths.
        """
        self.datasets = {}
        self.load_datasets(file_paths)

    def load_datasets(self, file_paths: Dict[str, str]) -> None:
        """
        Load datasets from CSV files and perform initial data type conversions.

        Args:
            file_paths (Dict[str, str]): A dictionary where keys are dataset names and values are file paths.
        """
        for name, path in file_paths.items():
            df = pd.read_csv(path)
            self.datasets[name] = self.convert_datatypes(df)

    def convert_datatypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert column datatypes to more appropriate types.

        Args:
            df (pd.DataFrame): The DataFrame to convert.

        Returns:
            pd.DataFrame: The DataFrame with converted datatypes.
        """
        for col in df.columns:
            # Convert date-like columns to datetime
            if df[col].dtype == 'object' and df[col].str.contains('-').any():
                df[col] = pd.to_datetime(df[col], errors='coerce')

            # Convert numeric-like columns to appropriate numeric types
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='raise')
                except ValueError:
                    pass  # Keep as object if conversion fails

        return df

    def get_dataset(self, name: str) -> pd.DataFrame:
        """
        Retrieve a dataset by name.

        Args:
            name (str): The name of the dataset to retrieve.

        Returns:
            pd.DataFrame: The requested dataset.

        Raises:
            KeyError: If the dataset name is not found.
        """
        if name not in self.datasets:
            raise KeyError(f"Dataset '{name}' not found.")
        return self.datasets[name]

    def filter_dataset(self, name: str, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter a dataset based on given conditions.

        Args:
            name (str): The name of the dataset to filter.
            conditions (Dict[str, Any]): A dictionary of column-value pairs to filter on.

        Returns:
            pd.DataFrame: The filtered dataset.
        """
        df = self.get_dataset(name)
        for col, value in conditions.items():
            if col in df.columns:
                df = df[df[col] == value]
        return df

    def multi_dataset_filter(self, dataset_conditions: Dict[str, Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
        """
        Filter multiple datasets based on given conditions.

        Args:
            dataset_conditions (Dict[str, Dict[str, Any]]): A dictionary where keys are dataset names
                and values are dictionaries of filtering conditions.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary of filtered datasets.
        """
        return {name: self.filter_dataset(name, conditions)
                for name, conditions in dataset_conditions.items()}

    def join_datasets(self, left: str, right: str, on: Union[str, List[str]], how: str = 'inner') -> pd.DataFrame:
        """
        Join two datasets.

        Args:
            left (str): Name of the left dataset.
            right (str): Name of the right dataset.
            on (Union[str, List[str]]): Column(s) to join on.
            how (str, optional): Type of join to perform. Defaults to 'inner'.

        Returns:
            pd.DataFrame: The joined dataset.
        """
        left_df = self.get_dataset(left)
        right_df = self.get_dataset(right)
        return pd.merge(left_df, right_df, on=on, how=how)

    def aggregate_dataset(self, name: str, group_by: Union[str, List[str]], agg_dict: Dict[str, str]) -> pd.DataFrame:
        """
        Aggregate a dataset.

        Args:
            name (str): Name of the dataset to aggregate.
            group_by (Union[str, List[str]]): Column(s) to group by.
            agg_dict (Dict[str, str]): Dictionary specifying aggregation functions for each column.

        Returns:
            pd.DataFrame: The aggregated dataset.
        """
        df = self.get_dataset(name)
        return df.groupby(group_by).agg(agg_dict).reset_index()

    def get_info(self, name: str) -> None:
        """
        Print information about a specific dataset.

        Args:
            name (str): Name of the dataset.
        """
        df = self.get_dataset(name)
        print(f"Dataset: {name}")
        print(df.info())
        print("\nSample data:")
        print(df.head())

    def get_column_unique_values(self, name: str, column: str) -> List[Any]:
        """
        Get unique values in a specific column of a dataset.

        Args:
            name (str): Name of the dataset.
            column (str): Name of the column.

        Returns:
            List[Any]: List of unique values in the specified column.
        """
        df = self.get_dataset(name)
        return df[column].unique().tolist()

# Example usage:
if __name__ == "__main__":
    file_paths = {
        'screening': '01_psscr_0924.csv',
        'interventions': '02_psint_0924.csv',
        'group_counseling': '03_psgc_0924.csv',
        'individual_counseling': '04_psic_0924.csv',
        'follow_up': '05_psfua_0924.csv',
        'pei': '06_pspei_0924.csv',
        'trw': '07_pstrw_0924.csv',
        'td': '08_pstd_0924.csv'
    }

    dm = DatasetManager(file_paths)

    # Get info about a specific dataset
    dm.get_info('screening')

    # Filter a dataset
    filtered_screening = dm.filter_dataset('screening', {'sc_loc': 'GTZ'})
    print(filtered_screening.head())

    # Filter multiple datasets
    multi_filtered = dm.multi_dataset_filter({
        'screening': {'sc_loc': 'GTZ'},
        'interventions': {'need_mhpss': 'Yes'}
    })
    for name, df in multi_filtered.items():
        print(f"\nFiltered {name}:")
        print(df.head())

    # Join datasets
    joined = dm.join_datasets('screening', 'interventions', on='rid')
    print("\nJoined dataset:")
    print(joined.head())

    # Aggregate data
    aggregated = dm.aggregate_dataset('screening', 'sc_loc', {'rid': 'count'})
    print("\nAggregated data:")
    print(aggregated)

    # Get unique values in a column
    unique_locations = dm.get_column_unique_values('screening', 'sc_loc')
    print("\nUnique locations:")
    print(unique_locations)