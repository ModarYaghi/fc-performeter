# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations (not directly used but often needed with pandas)
from pathlib import Path  # For handling file paths in a cross-platform way
from typing import Union, List, Dict, Optional, Callable, Any  # For type hinting
from collections import OrderedDict  # For maintaining order in dictionaries
import logging  # For logging messages and errors
import glob  # For file path pattern matching
import os  # For operating system dependent functionality

# Define a custom exception for data reading errors
class DataReaderError(Exception):
    """Custom exception for data reading errors."""
    pass

def read_and_concatenate_datasets(
        file_input: Union[str, Path, List[Union[str, Path]], Dict[str, Union[str, Path]]],  # Input can be a single path, list of paths, or dictionary of paths
        file_type: str = 'auto',  # Type of files to read, 'auto' for automatic detection
        concat_axis: int = 0,  # Axis for concatenation (0 for rows, 1 for columns)
        read_kwargs: Optional[Dict[str, Any]] = None,  # Additional keyword arguments for reading functions
        preprocess_func: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,  # Function to preprocess each DataFrame
        error_handling: str = 'raise',  # How to handle errors: 'raise', 'skip', 'return_none', or 'log'
        logger: Optional[logging.Logger] = None,  # Logger object for message logging
        recursive: bool = False,  # Whether to search for files recursively in directories
        file_pattern: Optional[str] = None,  # Glob pattern for filtering files in directories
        chunk_size: Optional[int] = None,  # Size of chunks for reading large files
        sample_size: Optional[int] = None,  # Number of rows to sample from each file
        post_concat_func: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None  # Function to process the concatenated DataFrame
) -> Union[pd.DataFrame, Dict[str, Any]]:
    """
    Read multiple datasets from various input types and concatenate them into a single DataFrame.

    Args:
        file_input (Union[str, Path, List[Union[str, Path]], Dict[str, Union[str, Path]]]):
            Input files or directories. Can be a single file/directory path, a list of paths, or a dictionary of paths.
        file_type (str): Type of files to read. Supported types: 'auto', 'csv', 'excel', 'parquet', 'json', 'hdf', 'feather', 'pickle'.
            'auto' will attempt to infer the file type from the extension. Defaults to 'auto'.
        concat_axis (int): Axis along which to concatenate (0 for rows, 1 for columns). Defaults to 0.
        read_kwargs (Optional[Dict[str, Any]]): Additional keyword arguments to pass to the pandas read function.
        preprocess_func (Optional[Callable[[pd.DataFrame], pd.DataFrame]]): Function to preprocess each DataFrame before concatenation.
        error_handling (str): How to handle errors when reading files. Options: 'raise', 'skip', 'return_none', 'log'. Defaults to 'raise'.
        logger (Optional[logging.Logger]): Logger object for logging messages.
        recursive (bool): Whether to search for files recursively in directories. Defaults to False.
        file_pattern (Optional[str]): Glob pattern for filtering files in directories. E.g., '*.csv' for CSV files only.
        chunk_size (Optional[int]): If set, reads files in chunks of specified size to handle large files.
        sample_size (Optional[int]): If set, randomly samples specified number of rows from each file before concatenation.
        post_concat_func (Optional[Callable[[pd.DataFrame], pd.DataFrame]]): Function to process the concatenated DataFrame.

    Returns:
        Union[pd.DataFrame, Dict[str, Any]]: Concatenated DataFrame containing data from all successfully read files,
        or a dictionary containing the DataFrame and additional metadata.

    Raises:
        DataReaderError: Custom exception for various data reading errors.
        ValueError: If invalid arguments are provided.

    Example:
        >>> files = ['data1.csv', 'data2.csv', 'data3.csv']
        >>> df = read_and_concatenate_datasets(files, file_type='auto', read_kwargs={'encoding': 'utf-8'})
    """
    # Set up logging if not provided
    if logger is None:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

    # Define supported file types and their corresponding pandas read functions
    supported_file_types = {
        'csv': pd.read_csv,
        'excel': pd.read_excel,
        'parquet': pd.read_parquet,
        'json': pd.read_json,
        'hdf': pd.read_hdf,
        'feather': pd.read_feather,
        'pickle': pd.read_pickle
    }

    # Validate the error handling option
    if error_handling not in ['raise', 'skip', 'return_none', 'log']:
        raise ValueError("error_handling must be 'raise', 'skip', 'return_none', or 'log'")

    # Resolve file paths from the input
    file_paths = _resolve_file_input(file_input, recursive, file_pattern)

    # Initialize read_kwargs if not provided
    read_kwargs = read_kwargs or {}

    # Initialize lists and dictionaries for storing results and metadata
    dataframes = []  # List to store individual DataFrames
    counts = OrderedDict()  # OrderedDict to maintain the order of file counts
    metadata = {
        'successful_reads': 0,
        'failed_reads': 0,
        'total_files': len(file_paths)
    }  # Dictionary to store metadata about the reading process

    # Iterate through each file path
    for file_path in file_paths:
        try:
            # Determine the file type (auto-detect if 'auto' is specified)
            file_type_to_use = _infer_file_type(file_path) if file_type == 'auto' else file_type

            # Check if the file type is supported
            if file_type_to_use not in supported_file_types:
                raise DataReaderError(f"Unsupported file type: {file_type_to_use}")

            # Get the appropriate read function for the file type
            read_func = supported_file_types[file_type_to_use]

            # Read the file, potentially in chunks
            df = _read_file(read_func, file_path, read_kwargs, chunk_size)

            # Sample the DataFrame if sample_size is specified
            if sample_size:
                df = df.sample(n=min(sample_size, len(df)), random_state=42)

            # Apply preprocessing function if provided
            if preprocess_func:
                df = preprocess_func(df)

            # Add the DataFrame to the list
            dataframes.append(df)

            # Record the count of rows or columns (depending on concat_axis)
            counts[str(file_path)] = len(df) if concat_axis == 0 else df.shape[1]

            # Update metadata
            metadata['successful_reads'] += 1

            # Log success message
            logger.info(f"Successfully read and processed: {file_path}")

        except Exception as e:
            # Update metadata for failed reads
            metadata['failed_reads'] += 1

            # Construct error message
            message = f"Error reading {file_path}: {str(e)}"

            # Handle the error according to the specified error_handling method
            _handle_error(error_handling, message, logger)

    # Check if any DataFrames were successfully read
    if not dataframes:
        logger.warning("No valid DataFrames to concatenate.")
        return None if error_handling == 'return_none' else pd.DataFrame()

    # Concatenate all DataFrames
    result = pd.concat(dataframes, axis=concat_axis, ignore_index=True)

    # Apply post-concatenation function if provided
    if post_concat_func:
        result = post_concat_func(result)

    # Calculate total count (rows or columns) in the result
    total_count = len(result) if concat_axis == 0 else result.shape[1]
    counts['Total'] = total_count
    metadata['counts'] = counts

    # Log concatenation results
    logger.info(f"Successfully concatenated {len(dataframes)} DataFrames.")
    logger.info(f"Total rows: {total_count}")

    # Return the result DataFrame and metadata
    return {'data': result, 'metadata': metadata}

def _resolve_file_input(file_input, recursive, file_pattern):
    """
    Resolve various types of file inputs into a list of file paths.

    Args:
        file_input: Input files or directories (str, Path, List, or Dict)
        recursive: Whether to search recursively in directories
        file_pattern: Glob pattern for filtering files

    Returns:
        List of resolved file paths
    """
    # Convert single string or Path input to a list
    if isinstance(file_input, (str, Path)):
        file_input = [file_input]

    resolved_paths = []
    for path in file_input:
        if isinstance(path, dict):
            # If the input is a dictionary, extend the list with its values
            resolved_paths.extend(path.values())
        elif os.path.isdir(path):
            # If the path is a directory, use glob to find matching files
            pattern = file_pattern or '*'
            glob_pattern = os.path.join(path, '**', pattern) if recursive else os.path.join(path, pattern)
            resolved_paths.extend(glob.glob(glob_pattern, recursive=recursive))
        else:
            # If it's a file path, add it directly to the list
            resolved_paths.append(path)

    return resolved_paths

def _infer_file_type(file_path):
    """
    Infer the file type from the file extension.

    Args:
        file_path: Path to the file

    Returns:
        Inferred file type as a string

    Raises:
        DataReaderError if the file type cannot be inferred
    """
    # Get the lowercase file extension
    ext = os.path.splitext(file_path)[1].lower()

    # Map file extensions to file types
    if ext in ['.csv', '.txt']:
        return 'csv'
    elif ext in ['.xls', '.xlsx', '.xlsm']:
        return 'excel'
    elif ext == '.parquet':
        return 'parquet'
    elif ext == '.json':
        return 'json'
    elif ext in ['.h5', '.hdf5']:
        return 'hdf'
    elif ext == '.feather':
        return 'feather'
    elif ext in ['.pkl', '.pickle']:
        return 'pickle'
    else:
        raise DataReaderError(f"Unable to infer file type for {file_path}")

def _read_file(read_func, file_path, read_kwargs, chunk_size):
    """
    Read a file using the specified read function, optionally in chunks.

    Args:
        read_func: Pandas read function to use
        file_path: Path to the file
        read_kwargs: Additional keyword arguments for the read function
        chunk_size: Size of chunks for reading large files

    Returns:
        Pandas DataFrame containing the file contents
    """
    if chunk_size:
        # Read the file in chunks
        chunks = []
        for chunk in read_func(file_path, chunksize=chunk_size, **read_kwargs):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)
    else:
        # Read the entire file at once
        return read_func(file_path, **read_kwargs)

def _handle_error(error_handling: str, message: str, logger: logging.Logger) -> None:
    """
    Handle errors based on the specified error_handling strategy.

    Args:
        error_handling: Error handling strategy ('raise', 'skip', 'return_none', or 'log')
        message: Error message to log or raise
        logger: Logger object for logging messages

    Raises:
        DataReaderError if error_handling is 'raise'
    """
    if error_handling == 'raise':
        logger.error(message)
        raise DataReaderError(message)
    elif error_handling == 'skip':
        logger.warning(message)
    elif error_handling == 'log':
        logger.error(message)
    else:  # 'return_none'
        logger.info(message)

# Example usage
if __name__ == "__main__":
    # Example 1: Reading from a directory
    result = read_and_concatenate_datasets(
        'path/to/data/directory',
        file_type='auto',
        recursive=True,
        file_pattern='*.csv',
        read_kwargs={'encoding': 'utf-8'},
        error_handling='skip'
    )
    print(result['data'].head())
    print(result['metadata'])

    # Example 2: Reading from a list of files
    files = ['data1.csv', 'data2.excel', 'data3.parquet']
    result = read_and_concatenate_datasets(
        files,
        file_type='auto',
        read_kwargs={'encoding': 'utf-8'},
        sample_size=1000,
        error_handling='log'
    )
    print(result['data'].head())
    print(result['metadata'])

    # Example 3: Reading from a dictionary of files
    file_dict = {'csv_file': 'data1.csv', 'excel_file': 'data2.xlsx'}
    result = read_and_concatenate_datasets(
        file_dict,
        file_type='auto',
        chunk_size=10000,
        preprocess_func=lambda df: df.dropna(),
        post_concat_func=lambda df: df.reset_index(drop=True)
    )
    print(result['data'].head())
    print(result['metadata'])