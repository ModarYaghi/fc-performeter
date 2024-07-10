import os
import logging
from typing import Dict, Union, List, Any
from io import BytesIO
import pandas as pd
import msoffcrypto
import concurrent.futures
import warnings
from pandas import DataFrame
from src.utils.decorator_funcs import progress_bar_decorator
# from utils.decorator_funcs import progress_bar_decorator


class ExcelFileDecryptionError(Exception):
    """Custom exception raised when an error occurs during the decryption of an Excel file."""

    pass


class ExcelFileReadError(Exception):
    """Custom exception raised when an error occurs while reading an Excel file."""

    pass


class ExcelDecryptorUtils:
    """
    Utility class providing static methods for decrypting Excel files.

    Methods:
    - decrypt_file: Decrypts a single Excel file given its path and password.
    """

    @staticmethod
    def decrypt_file(file_path: str, password: str) -> BytesIO:
        """
        Decrypts a single Excel file using the provided password.

        Parameters:
        - file_path (str): The path to the encrypted Excel file.
        - password (str): The password used for decryption.

        Returns:
        - BytesIO: An in-memory file-like object containing the decrypted Excel file.
        """
        try:
            with open(file_path, "rb") as f:
                crypto = msoffcrypto.OfficeFile(f)
                crypto.load_key(password=password)
                decrypted_file = BytesIO()
                crypto.decrypt(decrypted_file)
                decrypted_file.seek(0)
                return decrypted_file
        except Exception as e:
            raise ExcelFileDecryptionError(
                f"Decryption error for file {file_path}: {e}"
            )


class FileProcessor:
    """
    Class for processing Excel files, including reading sheets and converting data formats.

    Attributes:
    - output_format (str): The desired output format for the data ('pandas' or 'polars').

    Methods:
    - read_sheets_from_file: Reads all sheets from a decrypted Excel file and returns them as DataFrames.
    - convert_to_desired_format: Converts a DataFrame to the specified format.
    """

    def __init__(self, output_format: str = "pandas"):
        """
        Initializes the FileProcessor with the desired output format.

        Parameters:
        - output_format (str): Desired output format ('pandas' or 'polars').
        """
        self.output_format = output_format.lower()

    def read_sheets_from_file(
        self, decrypted_file: BytesIO
    ) -> Dict[str, Union[pd.DataFrame]]:
        """
        Reads all sheets from a decrypted Excel file and converts them to the specified format.

        Parameters:
        - decrypted_file (BytesIO): The decrypted Excel file.

        Returns:
        - Dict[str, Union[pd.DataFrame, pl.DataFrame]]: A dictionary of DataFrames with sheet names as keys.
        """
        xls = pd.ExcelFile(decrypted_file)
        sheets = {}
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            sheets[sheet_name] = self.convert_to_desired_format(df)
        return sheets

    def convert_to_desired_format(self, df: pd.DataFrame) -> Union[pd.DataFrame]:
        """
        Converts a DataFrame to the desired format.

        Parameters:
        - df (pd.DataFrame): The DataFrame to convert.

        Returns:
        - Union[pd.DataFrame, pl.DataFrame]: The converted DataFrame.
        """
        return df


class ExcelDecryptor:
    """
    Main class for decrypting and reading encrypted Excel files.

    Attributes:
    - directory (str): Directory containing the encrypted Excel files.
    - password_dict (Dict[str, str]): Dictionary mapping filenames to their respective passwords.
    - file_processor (FileProcessor): An instance of the FileProcessor class for handling file processing.

    Methods:
    - read_encrypted_excels: Reads and decrypts Excel files in the specified directory.
    - process_file: Processes a single file, decrypting and reading its contents.
    - print_data_structure: Prints the structure of the processed data.
    - display_result_structure: Displays the structure of the result dictionary.
    """

    def __init__(self, directory: str, password_dict: Dict[str, str], output_format: str = "pandas"):
        """
        Initializes the ExcelDecryptor with the specified directory, password dictionary, and output format.

        Parameters:
        - directory (str): Directory containing the encrypted Excel files.
        - password_dict (Dict[str, str]): Dictionary mapping filenames to their respective passwords.
        - output_format (str): Desired output format ('pandas' or 'polars').
        """
        self.directory = directory
        self.password_dict = password_dict
        self.file_processor = FileProcessor(output_format)
        self._processed_data = None

        # Suppress UserWarnings from openpyxl related to Data Validation features
        warnings.filterwarnings("ignore", category=UserWarning)

    @progress_bar_decorator
    def read_encrypted_excels(self, selected_files: List[str] = None, progress_tracker=None) -> dict[str | Any, Any]:
        """
        Reads and decrypts selected Excel files in the specified directory, updating a progress bar for each file
        processed.

        This method is decorated with progress_bar_decorator, which injects a ProgressTracker instance. The method
        updates the progress bar after the completion of processing each file. It ensures the progress bar accurately
        reflects the processing status.

        Parameters:
            selected_files (List[str], optional): Filenames to process. If None, process all files.
            progress_tracker (ProgressTracker, optional): An instance of ProgressTracker for updating progress.

        Returns:
            DataFrame: A DataFrame displaying the files and sheets processed.

        Detailed Explanation:
            - The method uses a ThreadPoolExecutor to process files concurrently.
            - After submitting each file for processing, the method waits for its completion.
            - Upon completion, the progress_tracker.update() is called to increment the progress bar.
            - This update reflects the real-time progress of file processing within the ThreadPoolExecutor.
        """
        processed_data = {}
        files_to_process = (self.password_dict.keys() if selected_files is None else selected_files)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.process_file, file, self.password_dict[file]): file
                for file in files_to_process
            }

            for future in concurrent.futures.as_completed(futures):
                file = futures[future]
                try:
                    result = future.result()
                    if result is not None:
                        processed_data[file] = result
                except Exception as e:
                    # Handle exceptions if necessary
                    print(f"exception in {file}: {e}")

                # Update the progress tracker after each file is processed
                if progress_tracker:
                    progress_tracker.update()

        self._processed_data = processed_data
        return processed_data

    def process_file(self, file: str, password: str) -> Union[Dict[str, Union[pd.DataFrame]], None]:
        """
        Processes a single file, decrypting it and reading its contents.

        Parameters:
        - file (str): The filename of the Excel file to process.
        - password (str): The password for decrypting the file.

        Returns: - Union[Dict[str, Union[pd.DataFrame, pl.DataFrame]], None]: A dictionary of DataFrames for each
        sheet in the file, or None if an error occurred.
        """
        file_path = os.path.join(self.directory, file)
        if not os.path.exists(file_path):
            logging.warning(f"File {file_path} does not exist. Skipping.")
            return None

        try:
            decrypted_file = ExcelDecryptorUtils.decrypt_file(file_path, password)
            sheets = self.file_processor.read_sheets_from_file(decrypted_file)
            return sheets
        except ExcelFileDecryptionError as e:
            logging.error(f"Decryption error for file {file_path}: {e}")
            return None
        except ExcelFileReadError as e:
            logging.error(f"File read error for file {file_path}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unhandled error processing file {file_path}: {e}")
            return None

    @property
    def print_data_structure(self):
        """
        Prints the structure of the processed data.

        Returns:
        - str: A string representation of the processed data structure, or a message if no data has been processed yet.
        """
        if self._processed_data is not None:
            return self.display_result_structure(self._processed_data)
        else:
            return "Data has not been processed yet."

    @staticmethod
    def display_result_structure(processed_data: Dict[str, Dict[str, Union[pd.DataFrame]]]) -> pd.DataFrame:
        """
        Creates a DataFrame displaying the structure of the result dictionary.

        Parameters:
        - processed_data (Dict[str, Dict[str, Union[pd.DataFrame, pl.DataFrame]]]): The processed data.

        Returns:
        - pd.DataFrame: A DataFrame displaying the files and sheets processed.
        """
        data = [
            (file, sheet)
            for file, sheets in processed_data.items()
            for sheet in sheets.keys()
        ]
        return pd.DataFrame(data, columns=["File", "Sheet"])


# Example usage:
# decryptor = ExcelDecryptor("path_to_directory", {"file1.xlsx": "password1", "file2.xlsx": "password2"}, "pandas")
# decrypted_data = decryptor.read_encrypted_excels(["file1.xlsx"])
# print(decryptor.print_data_structure)

if __name__ == "__main__":
    # Example usage of ExcelDecryptor
    decryptor = ExcelDecryptor(
        "path_to_directory",
        {"file1.xlsx": "password1", "file2.xlsx": "password2"},
        "pandas",
    )
    decrypted_data = decryptor.read_encrypted_excels(["file1.xlsx"])
    print(decryptor.print_data_structure)
    pass
