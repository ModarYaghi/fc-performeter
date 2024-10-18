import pandas as pd
from typing import Union, List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def count_dates_in_range(
        data: Union[str, pd.DataFrame, List[Union[str, pd.DataFrame]]],
        id_columns: Union[str, List[str]],
        date_columns: Union[List[str], List[List[str]]],
        start_date: str,
        end_date: str
) -> Dict[str, Dict[str, int]]:
    """
    Count total dates and unique dates per ID within a specified range for each dataset and in total.

    Args:
        data (Union[str, pd.DataFrame, List[Union[str, pd.DataFrame]]]):
            Path(s) to dataset(s) or DataFrame(s).
        id_columns (Union[str, List[str]]):
            Name(s) of ID column(s) for each dataset.
        date_columns (Union[List[str], List[List[str]]]):
            List of date column names for each dataset.
        start_date (str): Start date of the range (inclusive).
        end_date (str): End date of the range (inclusive).

    Returns:
        Dict[str, Dict[str, int]]: Dictionary containing count of total dates and unique dates per ID for each dataset and total.
    """

    def process_single_dataset(
            df: pd.DataFrame,
            id_col: str,
            date_cols: List[str]
    ) -> Dict[str, int]:
        """
        Process a single dataset and return counts of total and unique dates in range.

        Args:
            df (pd.DataFrame): DataFrame to process.
            id_col (str): Name of the ID column.
            date_cols (List[str]): List of date column names.

        Returns:
            Dict[str, int]: Count of total dates and unique dates per ID.
        """
        try:
            # Combine all date columns
            all_dates = pd.concat([df[col] for col in date_cols])

            # Convert to datetime and filter by date range
            all_dates = pd.to_datetime(all_dates, errors='coerce')
            mask = (all_dates >= start_date) & (all_dates <= end_date)
            filtered_dates = all_dates[mask]

            # Count total dates in range
            total_dates_count = filtered_dates.count()

            # Count unique dates per ID (considering only unique dates per ID)
            df_filtered = df.loc[filtered_dates.index.intersection(df.index)]
            unique_dates_count = df_filtered.groupby(id_col).apply(
                lambda group: pd.to_datetime(group[date_cols].stack(), errors='coerce').nunique()
            ).sum()

            return {
                'total_dates_count': total_dates_count,
                'unique_dates_count': unique_dates_count
            }

        except Exception as e:
            logger.error(f"Error processing dataset: {e}")
            return {
                'total_dates_count': 0,
                'unique_dates_count': 0
            }

    # Ensure data, id_columns, and date_columns are lists for uniform processing
    if not isinstance(data, list):
        data = [data]
    if not isinstance(id_columns, list):
        id_columns = [id_columns]
    if not isinstance(date_columns[0], list):
        date_columns = [date_columns]

    # Validate that input lengths match
    if len(data) != len(id_columns) or len(data) != len(date_columns):
        raise ValueError("Mismatched input lengths: data, id_columns, and date_columns must have the same length.")

    # Initialize results dictionary
    results = {}
    total_dates_count_all = 0
    unique_dates_count_all = 0

    # Process each dataset
    for i, (dataset, id_col, date_cols) in enumerate(zip(data, id_columns, date_columns)):
        try:
            # Load dataset if it's a file path
            if isinstance(dataset, str):
                logger.info(f"Loading dataset from {dataset}")
                df = pd.read_csv(dataset)
            else:
                df = dataset

            # Process the dataset
            logger.info(f"Processing Dataset_{i + 1}")
            counts = process_single_dataset(df, id_col, date_cols)

            # Store the results
            results[f"Dataset_{i + 1}"] = counts
            total_dates_count_all += counts['total_dates_count']
            unique_dates_count_all += counts['unique_dates_count']

        except FileNotFoundError:
            logger.error(f"File not found: {dataset}")
        except pd.errors.EmptyDataError:
            logger.error(f"Empty data: {dataset}")
        except Exception as e:
            logger.error(f"Unexpected error processing Dataset_{i + 1}: {e}")

    # Add total counts for all datasets
    results["Total"] = {
        'total_dates_count': total_dates_count_all,
        'unique_dates_count': unique_dates_count_all
    }

    return results

# Example Usage
if __name__ == "__main__":
    try:
        result = count_dates_in_range(
            data=['data1.csv', 'data2.csv'],
            id_columns=['id_col1', 'id_col2'],
            date_columns=[['date1', 'date2'], ['date3']],
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        print(result)
    except ValueError as ve:
        logger.error(f"Input error: {ve}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
