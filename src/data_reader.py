import os

import pandas as pd
# import json
import yaml
import logging
from typing import Any, Dict, List, Optional, Tuple

from pandas import DataFrame

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class YAMLDataReader:
    """
        A class to read and process data from a YAML file.

    Attributes:
    -----------
    data_source : List[Dict[str, Any]]
        A list of dictionaries, each representing a data source entry.
    structure : List[Dict[str, Any]]
        A list of dictionaries, each representing a dataset and its variables.

    Methods:
    --------
    get_data_source() -> List[Dict[str, Any]]:
        Returns the data source section of the YAML file.
    get_structure() -> List[Dict[str, Any]]:
        Returns the structure section of the YAML file.
    get_password_for_file(file_name: str) -> Optional[str]:
        Returns the password for a specified file, if available.
    get_files_by_service(service_name: str) -> List[Dict[str, Any]]:
        Returns a list of files associated with a specific service.
    get_variables_by_dataset(dataset_name: str) -> List[Dict[str, Any]]:
        Retrieves variables for a given dataset name.
    search_variables(search_term: str) -> List[Tuple[str, Dict[str, Any]]]:
        Searches for variables across all datasets containing a specific term.
    """

    def __init__(self, file_path: str):
        """
        Initializes the YAMLDataReader with data from the given YAML file.

        Parameters:
        -----------
        file_path : str
            The path to the YAML file to be read.

        Raises:
        -------
        FileNotFoundError:
            If the specified file does not exist.
        yaml.YAMLError:
            If the YAML file cannot be parsed.
        """
        try:
            with open(file_path, "r") as file:
                data = yaml.safe_load(file)

            # Initialize each section of the YAML file.
            self.data_types = data.get("data_types", [])
            self.sheets = data.get("sheets_names", [])
            self.data_source = data.get("data_source", [])
            self.datasets = data.get("datasets", [])
            self.structure = self.get_structure()

        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")

    # def get_data_source(self) -> List[Dict[str, Any]]:
    #     """Returns the data source section of the YAML file."""
    #     return self.data_source
    #
    # def get_data_type(self, type: str) -> Dict[str, Any]:
    #     """Returns a data type."""
    #     return self.data_types[type]
    #
    def get_structure(self) -> DataFrame:
        """Returns the structure section of the YAML file."""
        formatted_data = []

        for dataset_dict in self.datasets:
            dataset_name = dataset_dict["dataset"]
            for var_info in dataset_dict["variables"]:
                formatted_data.append({
                    "Dataset": dataset_name,
                    "Variable": var_info["var"],
                    "Type": var_info["type"],
                    "Level": var_info["level"]
                })
        return pd.DataFrame(formatted_data)

    def get_password_for_file(self, file_name: str) -> Optional[str]:
        """
        Returns the password for a specified file, if available.

        Parameters:
        -----------
        file_name : str
            The name of the file for which the password is needed.

        Returns:
        --------
        Optional[str]:
            The password if found, otherwise None.
        """
        for entry in self.data_source:
            if entry["file"] == file_name:
                return entry["password"]
        return None

    def get_files_by_service(self, service_name: str) -> List[Dict[str, Any]]:
        """
        Returns a list of files associated with a specific service.

        Parameters:
        -----------
        service_name : str
            The name of the service.

        Returns:
        --------
        List[Dict[str, Any]]:
            A list of file entries for the specified service.
        """
        return [entry for entry in self.data_source if entry["service"] == service_name]

    def get_variables_by_dataset(self, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Retrieves variables for a given dataset name.

        Parameters:
        -----------
        dataset_name : str
            The name of the dataset.

        Returns:
        --------
        List[Dict[str, Any]]:
            A list of variables for the specified dataset.
        """
        for dataset in self.datasets:
            if dataset["dataset"] == dataset_name:
                return dataset.get("variables", [])
        return []

    def get_variable_names_by_dataset(self, dataset_name: str) -> List[str]:
        """
        Retrieves the names of variables for a given dataset.

        Args:
        - dataset_name (str): The name of the dataset.

        Returns:
        - List[str]: A list of variable names in the specified dataset.
        """
        variables_info = self.get_variables_by_dataset(dataset_name)
        return [variable["var"] for variable in variables_info]

    # TODO: Make the methods accept a list of levels/types
    def get_variable_names_by_dataset_and_level(
            self, dataset_name: str, level: int
    ) -> List[str]:
        """
        Retrieves names of variables for a given dataset and level.

        Args:
        - dataset_name (str): The name of the dataset.
        - level (int): The specific level of the variables.

        Returns:
        - List[str]: A list of variable names in the specified dataset with the specified level.
        """
        variables_info = self.get_variables_by_dataset(dataset_name)
        return [
            variable["var"]
            for variable in variables_info
            if variable.get("level") == level
        ]

    def get_variable_names_by_dataset_and_type(
            self, dataset_name: str, var_type: str
    ) -> List[str]:
        """
        Retrieves names of variables for a given dataset and type.

        Args:
        - dataset_name (str): The name of the dataset.
        - var_type (str): The specific type of the variables.

        Returns:
        - List[str]: A list of variable names in the specified dataset with the specified type.
        """
        variables_info = self.get_variables_by_dataset(dataset_name)
        return [
            variable["var"]
            for variable in variables_info
            if variable.get("type") == var_type
        ]

    def search_variables(self, search_term: str) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Searches for variables across all datasets containing a specific term.

        Parameters:
        -----------
        search_term : str
            The term to search for within variable names.

        Returns:
        --------
        List[Tuple[str, Dict[str, Any]]]:
            A list of tuples, each containing the dataset name and the variable
            where the search term was found.
        """
        results = []
        for dataset in self.datasets:
            for variable in dataset.get(
                    "variables", []
            ):  # Ensures 'variables' key exists
                if (
                        "var" in variable and search_term in variable["var"]
                ):  # Check if 'var' key exists
                    results.append((dataset["dataset"], variable))
        return results

    def get_excel_passwords_by_directory(self, directory: str) -> Dict[str, str]:
        """
        Retrieves passwords for Excel files in the specified directory.

        Parameters:
        - directory (str): The directory containing Excel files.

        Returns:
        - Dict[str, str]: A dictionary mapping Excel file names to their passwords.
        """
        passwords = {}
        for file in os.listdir(directory):
            if file.endswith(".xlsx"):
                pw = self.get_password_for_file(file)
                if pw is not None:
                    passwords[file] = pw
                else:
                    print(f"No password for {file}")
        return passwords


# class JSONDataReader:
#     """
#     A class to read and process data from a JSON file.
#     """
#
#     def __init__(self, file_path: str):
#         """
#         Initializes the JSONDataReader with data from the given JSON file.
#         """
#         self.data = self._load_json(file_path)
#
#     @staticmethod
#     def _load_json(file_path: str) -> Dict[str, Any]:
#         """
#         Loads and parses the JSON file.
#         """
#         try:
#             with open(file_path, "r") as file:
#                 return json.load(file)
#         except FileNotFoundError:
#             logging.error(f"The file {file_path} was not found.")
#             raise
#         except json.JSONDecodeError as e:
#             logging.error(f"Error parsing JSON file: {e}")
#             raise
#
#     def get_section(self, section_name: str) -> List[Dict[str, Any]]:
#         """
#         Returns a specific section from the JSON file.
#         """
#         return self.data.get(section_name, [])
#
#     def get_password_for_file(self, file_name: str) -> Optional[str]:
#         """
#         Returns the password for a specified file, if available.
#         """
#         return next(
#             (
#                 entry["password"]
#                 for entry in self.get_section("data_source")
#                 if entry.get("file") == file_name
#             ),
#             None,
#         )
#
#     def get_files_by_scope(self, service_name: str) -> List[str]:
#         """
#         Returns a list of file names associated with a specific scope (pss, pt, referring, tracker_td).
#         """
#         return [
#             entry["file"]
#             for entry in self.get_section("data_source")
#             if entry.get("scope") == service_name
#         ]
#
#     def get_variables_by_dataset(self, dataset_name: str) -> List[Dict[str, Any]]:
#         """
#         Retrieves variables for a given dataset name.
#         """
#         return next(
#             (
#                 dataset["variables"]
#                 for dataset in self.get_section("datasets")
#                 if dataset.get("dataset") == dataset_name
#             ),
#             [],
#         )
#
#     def search_variables(self, search_term: str) -> List[Tuple[str, Dict[str, Any]]]:
#         """
#         Searches for variables across all datasets containing a specific term.
#         """
#         return [
#             (dataset["dataset"], var)
#             for dataset in self.get_section("datasets")
#             for var in dataset.get("variables", [])
#             if search_term in var.get("var", "")
#         ]
#
#     def get_excel_passwords_by_directory(self, directory: str) -> Dict[str, str]:
#         """
#         Retrieves passwords for Excel files in the specified directory.
#         """
#         excel_files = [file for file in os.listdir(directory) if file.endswith(".xlsx")]
#         return {file: self.get_password_for_file(file) or "" for file in excel_files}
#


if __name__ == "__main__":
    pass
