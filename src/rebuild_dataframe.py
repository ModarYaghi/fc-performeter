import pandas as pd
import numpy as np
from typing import Dict, Any, Callable
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def merge_strategy(
    column_values: pd.Series, column_name: str, strategies: Dict[str, Any]
) -> Any:
    """Apply merge strategy for a given column."""
    if column_name in strategies:
        return strategies[column_name](column_values)
    elif "Yes" in column_values.values:
        return "Yes"
    elif column_values.dtype == "object":
        return next((v for v in column_values if pd.notna(v)), np.nan)
    elif pd.api.types.is_numeric_dtype(column_values):
        return np.nanmax(column_values)
    elif pd.api.types.is_datetime64_any_dtype(column_values):
        return pd.to_datetime(column_values).max()
    else:
        logger.warning(
            f"No specific merge strategy for column {column_name}. Using first non-null value."
        )
        return next((v for v in column_values if pd.notna(v)), np.nan)


def rebuild_dataframe(
    df: pd.DataFrame,
    id_column: str,
    merge_strategies: Dict[str, Callable] = None,
    chunk_size: int = None,
) -> pd.DataFrame:
    """
    Rebuild a dataframe by merging duplicate records based on an ID column.

    Args:
    df (pd.DataFrame): Input DataFrame
    id_column (str): Name of the ID column
    merge_strategies (Dict[str, Callable]): Custom merge strategies for specific columns
    chunk_size (int): Number of unique IDs to process at a time. If None, process all at once.

    Returns:
    pd.DataFrame: Rebuilt DataFrame with duplicates merged
    """
    merge_strategies = merge_strategies or {}

    # Verify input
    if id_column not in df.columns:
        raise ValueError(f"ID column '{id_column}' not found in DataFrame")

    # Create an empty dataframe with the same structure and dtypes
    empty_df = pd.DataFrame(columns=df.columns).astype(df.dtypes)

    # Get unique IDs
    unique_ids = df[id_column].unique()

    # Process in chunks if specified
    if chunk_size:
        id_chunks = [
            unique_ids[i : i + chunk_size]
            for i in range(0, len(unique_ids), chunk_size)
        ]
    else:
        id_chunks = [unique_ids]

    total_records = 0
    for chunk in id_chunks:
        chunk_df = df[df[id_column].isin(chunk)]

        # Group by ID and apply merge strategy
        grouped = chunk_df.groupby(id_column)
        merged_records = grouped.apply(
            lambda x: pd.Series(
                {
                    col: merge_strategy(x[col], col, merge_strategies)
                    for col in df.columns
                }
            )
        )

        # Append to the result DataFrame
        empty_df = pd.concat(
            [empty_df, merged_records.reset_index(drop=True)], ignore_index=True
        )

        total_records += len(merged_records)
        logger.info(f"Processed {total_records} records so far.")

    # Verify the rebuild
    if len(empty_df) != len(unique_ids):
        logger.warning(
            f"Mismatch in record count. Expected {len(unique_ids)}, got {len(empty_df)}"
        )

    return empty_df


# Example usage
if __name__ == "__main__":
    # Sample DataFrame
    # df = pd.DataFrame({
    #     'id': [1, 1, 2, 3, 3],
    #     'name': ['John', 'Johnny', 'Alice', 'Bob', 'Robert'],
    #     'age': [30, np.nan, 25, 40, 41],
    #     'has_car': ['Yes', 'No', 'No', 'Yes', np.nan],
    #     'salary': [50000, 55000, 60000, np.nan, 70000],
    #     'last_visit': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'])
    # })

    # print("Original DataFrame:")
    # print(df)

    # # Custom merge strategies
    # custom_strategies = {
    #     'name': lambda x: ' '.join(x.dropna().unique()),  # Combine names
    #     'salary': np.nanmean  # Use mean for salary instead of max
    # }

    # rebuilt_df = rebuild_dataframe(df, 'id', merge_strategies=custom_strategies, chunk_size=2)

    # print("\nRebuilt DataFrame:")
    # print(rebuilt_df)

    # # Verify data types
    # print("\nData Types:")
    # print(rebuilt_df.dtypes)
    pass
