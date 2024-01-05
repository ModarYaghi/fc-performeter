import pandas as pd

from src.data_reader import YAMLDataReader


class Dataset:
    """Interface for a dataset."""

    def __init__(self, config_path: str, dataset: str):
        # Initialize the dataset.
        self.config_path = config_path
        self.dataset = dataset

        # Load the dataset configuration.
        self.config = YAMLDataReader(self.config_path)

        # Get the variable names for the dataset.
        self.vars = self.config.get_variable_names_by_dataset(self.dataset)

        # Get the variable names for the dataset at level 0.
        self.bvars = self.config.get_variable_names_by_dataset_and_level(
            self.dataset, 0
        )

        # Get the variable names for the dataset of type datetime64[ns].
        self.dvars = self.config.get_variable_names_by_dataset_and_type(
            self.dataset, "datetime64[ns]"
        )

        # Get the variable names for the dataset of type Int64.
        self.ivars = self.config.get_variable_names_by_dataset_and_type(
            self.dataset, "Int64"
        )

        self.svars = self.config.get_variable_names_by_dataset_and_type(
            self.dataset, "StringDtype"
        )

        self.cvars = self.config.get_variable_names_by_dataset_and_type(
            self.dataset, "category"
        )

        self.bovars = self.config.get_variable_names_by_dataset_and_type(
            self.dataset, "boolean"
        )


def dttrans(
    dataframe: pd.DataFrame,
    dataset: Dataset = None,
    config_path: str = None,
    dataset_name: str = None,
):
    if dataset is None:
        dataset = Dataset(config_path, dataset_name)

    if dataset.dvars:
        dataframe[dataset.dvars] = dataframe[dataset.dvars].apply(pd.to_datetime)
