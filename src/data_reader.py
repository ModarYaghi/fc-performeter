import os
import yaml
import logging
import msoffcrypto
import pandas as pd
import polars as pl
from tqdm import tqdm
from io import BytesIO
from typing import Any, Dict, List, Union, Optional, Tuple

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ExcelFileDecryptionError(Exception):
    """Custom exception for decryption errors."""
    pass


class ExcelFileReadError(Exception):
    """Custom exception for file read errors."""
    pass


class ExcelDecryptor:
    """
    A class for decrypting and reading encrypted Excel files.

    Attributes:
    - directory (str): Directory containing the encrypted Excel files.
    - password_dict (Dict[str, str]): Dictionary mapping filenames to their respective passwords.
    - output_format (str): Desired output format ('pandas' or 'polars'). Default is 'pandas'.

    Methods:
    - __init__: Initializes the ExcelDecryptor with a directory, password dictionary, and output format.
    - read_encrypted_excels: Reads and decrypts Excel files in the specified directory, returning a dictionary of DataFrames.
    - decrypt_file: Decrypts a single Excel file given its path and password.
    - read_sheets_from_file: Reads all sheets from a decrypted Excel file and returns them as DataFrames.
    - convert_to_desired_format: Converts a DataFrame to the desired format (Pandas or Polars).
    - calculate_total_sheets: Calculates the total number of sheets in all Excel files to be processed.
    - display_result_structure: Displays the structure of the result dictionary from read_encrypted_excels method.
    """

    def __init__(self, directory: str, password_dict: Dict[str, str], output_format: str = 'pandas'):
        """
        Initializes the ExcelDecryptor with the specified directory, password dictionary, and output format.

        Parameters:
        - directory (str): Directory containing the encrypted Excel files.
        - password_dict (Dict[str, str]): Dictionary mapping filenames to their respective passwords.
        - output_format (str): Desired output format ('pandas' or 'polars').
        """
        self.directory = directory
        self.password_dict = password_dict
        self.output_format = output_format.lower()
        self._processed_data = None

    # TODO: Add option to read all sheets or specific sheets
    def read_encrypted_excels(self) -> Dict[str, Dict[str, Union[pd.DataFrame, pl.DataFrame]]]:
        """
        Reads and decrypts Excel files in the specified directory.

        Returns:
        - Dict[str, Dict[str, Union[pd.DataFrame, pl.DataFrame]]]: A dictionary where the keys are filenames
          and the values are another dictionary with sheet names as keys and DataFrames as values.
        """
        processed_data = {}
        total_sheets = self.calculate_total_sheets()
        logging.info(f"Processing {total_sheets} sheets across all files.")

        for file, password in tqdm(self.password_dict.items(), desc="Decrypting and Reading Files"):
            file_path = os.path.join(self.directory, file)
            if not os.path.exists(file_path):
                logging.error(f"File {file_path} does not exist.")
                continue

            try:
                decrypted_file = self.decrypt_file(file_path, password)
                sheets = self.read_sheets_from_file(decrypted_file)
                processed_data[file] = sheets
            except msoffcrypto.exceptions.DecryptionError as e:
                logging.error(f"Decryption error for file {file_path}: {e}")
                raise ExcelFileDecryptionError(f"Decryption error for file {file_path}: {e}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                raise ExcelFileReadError(f"Error processing file {file_path}: {e}")

        self._processed_data = processed_data
        return processed_data

    @staticmethod
    def decrypt_file(file_path: str, password: str) -> BytesIO:
        """
        Decrypts a single Excel file.

        Parameters:
        - file_path (str): Path to the encrypted Excel file.
        - password (str): Password for decryption.

        Returns:
        - BytesIO: A decrypted file object.
        """
        with open(file_path, "rb") as f:
            crypto = msoffcrypto.OfficeFile(f)
            crypto.load_key(password=password)
            decrypted_file = BytesIO()
            crypto.decrypt(decrypted_file)
            decrypted_file.seek(0)
            return decrypted_file

    def read_sheets_from_file(self, decrypted_file: BytesIO) -> Dict[str, Union[pd.DataFrame, pl.DataFrame]]:
        """
        Reads all sheets from a decrypted Excel file.

        Parameters:
        - decrypted_file (BytesIO): A decrypted Excel file object.

        Returns:
        - Dict[str, Union[pd.DataFrame, pl.DataFrame]]: Dictionary with sheet names as keys and DataFrames as values.
        """
        xls = pd.ExcelFile(decrypted_file)
        sheets = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            sheets[sheet_name] = self.convert_to_desired_format(df)
        return sheets

    def convert_to_desired_format(self, df: pd.DataFrame) -> Union[pd.DataFrame, pl.DataFrame]:
        """
        Converts a DataFrame to the desired format (Pandas or Polars).

        Parameters:
        - df (pd.DataFrame): The DataFrame to convert.

        Returns:
        - Union[pd.DataFrame, pl.DataFrame]: Converted DataFrame.
        """
        if self.output_format == 'polars':
            return pl.from_pandas(df)
        return df

    def calculate_total_sheets(self) -> int:
        """
        Calculates the total number of sheets in all Excel files to be processed.

        Returns:
        - int: Total number of sheets.
        """
        total_sheets = 0
        for file, password in self.password_dict.items():
            file_path = os.path.join(self.directory, file)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    crypto = msoffcrypto.OfficeFile(f)
                    crypto.load_key(password=password)
                    decrypted_file = BytesIO()
                    crypto.decrypt(decrypted_file)
                    decrypted_file.seek(0)
                    xls = pd.ExcelFile(decrypted_file)
                    total_sheets += len(xls.sheet_names)
        return total_sheets

    @property
    def print_data_structure(self):
        """
        Returns a DataFrame displaying the structure of the processed data.
        """
        if self._processed_data is not None:
            return self.display_result_structure(self._processed_data)
        else:
            return "Data has not been processed yet."

    @staticmethod
    def display_result_structure(processed_data: Dict[str, Dict[str, Union[pd.DataFrame, pl.DataFrame]]]):
        """
        Creates a DataFrame displaying the structure of the result dictionary.

        Parameters:
            - result (Dict[str, Dict[str, Union[pd.DataFrame, pl.DataFrame]]]):
                The result dictionary from read_encrypted_excels method.

        Returns:
            - pd.DataFrame: A DataFrame displaying the files and sheets processed.
            """
        data = [(file, sheet) for file, sheets in processed_data.items() for sheet in sheets.keys()]
        df = pd.DataFrame(data, columns=["File", "Sheet"])
        return df


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
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            self.data_source = data.get('data_source', [])
            self.datasets = data.get('datasets', [])
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")

    def get_data_source(self) -> List[Dict[str, Any]]:
        """Returns the data source section of the YAML file."""
        return self.data_source

    def get_structure(self) -> List[Dict[str, Any]]:
        """Returns the structure section of the YAML file."""
        return self.datasets

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
            if entry['file'] == file_name:
                return entry['password']
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
        return [entry for entry in self.data_source if entry['service'] == service_name]

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
            if dataset['dataset'] == dataset_name:
                return dataset.get('variables', [])
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
        return [variable['var'] for variable in variables_info]

    # TODO: Make the methods accept a list of levels/types
    def get_variable_names_by_dataset_and_level(self, dataset_name: str, level: int) -> List[str]:
        """
        Retrieves names of variables for a given dataset and level.

        Args:
        - dataset_name (str): The name of the dataset.
        - level (int): The specific level of the variables.

        Returns:
        - List[str]: A list of variable names in the specified dataset with the specified level.
        """
        variables_info = self.get_variables_by_dataset(dataset_name)
        return [variable['var'] for variable in variables_info if variable.get('level') == level]

    def get_variable_names_by_dataset_and_type(self, dataset_name: str, var_type: str) -> List[str]:
        """
        Retrieves names of variables for a given dataset and type.

        Args:
        - dataset_name (str): The name of the dataset.
        - var_type (str): The specific type of the variables.

        Returns:
        - List[str]: A list of variable names in the specified dataset with the specified type.
        """
        variables_info = self.get_variables_by_dataset(dataset_name)
        return [variable['var'] for variable in variables_info if variable.get('type') == var_type]

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
            for variable in dataset.get('variables', []):  # Ensures 'variables' key exists
                if 'var' in variable and search_term in variable['var']:  # Check if 'var' key exists
                    results.append((dataset['dataset'], variable))
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
            if file.endswith('.xlsx'):
                pw = self.get_password_for_file(file)
                if pw is not None:
                    passwords[file] = pw
                else:
                    print(f'No password for {file}')
        return passwords


if __name__ == "__main__":
    # Example usage of ExcelDecryptor
    decryptor = ExcelDecryptor('path_to_directory',
                               {'file1.xlsx': 'password1', 'file2.xlsx': 'password2'}, 'polars')
    try:
        result = decryptor.read_encrypted_excels()
        print("Decryption and reading successful. Processed data:")
        print(result)
    except (ExcelFileDecryptionError, ExcelFileReadError) as e:
        print(f"An error occurred: {e}")

    # Example usage of YAMLDataReader
    yaml_reader = YAMLDataReader('path_to_yaml_file.yaml')
    data_source = yaml_reader.get_data_source()
    print("YAML Data Source section:")
    print(data_source)
