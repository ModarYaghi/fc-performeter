import pandas as pd
from typing import Union, List, Dict, Tuple

def count_dates_in_range(
        data: Union[str, pd.DataFrame, List[Union[str, pd.DataFrame]]],
        id_columns: Union[str, List[str]],
        date_columns: Union[List[str], List[List[str]]],
        start_date: str,
        end_date: str
) -> Dict[str, int]:
    """
    Count unique dates within a specified range for each dataset and in total.

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
    Dict[str, int]: Dictionary with count of unique dates for each dataset and total.
    """

    def process_single_dataset(
            df: pd.DataFrame,
            id_col: str,
            date_cols: List[str]
    ) -> int:
        """
        Process a single dataset and return the count of unique dates in range.
        """
        # Combine all date columns
        all_dates = pd.concat([df[col] for col in date_cols])

        # Convert to datetime and filter by date range
        all_dates = pd.to_datetime(all_dates, errors='coerce')
        mask = (all_dates >= start_date) & (all_dates <= end_date)
        filtered_dates = all_dates[mask]

        # Count unique dates per ID
        unique_dates = filtered_dates.groupby(df[id_col].reindex(filtered_dates.index)).nunique()

        return unique_dates.sum()

    # Ensure data and id_columns are lists
    if not isinstance(data, list):
        data = [data]
    if not isinstance(id_columns, list):
        id_columns = [id_columns]
    if not isinstance(date_columns[0], list):
        date_columns = [date_columns]

    # Ensure all inputs have the same length
    assert len(data) == len(id_columns) == len(date_columns), "Mismatched input lengths"

    results = {}
    total_count = 0

    for i, (dataset, id_col, date_cols) in enumerate(zip(data, id_columns, date_columns)):
        # Load dataset if it's a file path
        if isinstance(dataset, str):
            df = pd.read_csv(dataset)
        else:
            df = dataset

        # Process the dataset
        count = process_single_dataset(df, id_col, date_cols)
        results[f"Dataset_{i+1}"] = count
        total_count += count

    results["Total"] = total_count

    return results
