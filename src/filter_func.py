import pandas as pd
from datetime import datetime, timedelta


def filter_by_date(df, date_column, start_date=None, end_date=None, specific_date=None,
                   last_n_days=None, date_range=None, custom_filter=None):
    """
    Filters a DataFrame based on various date filtering criteria.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter.
    - date_column (str): The name of the column containing date information.
    - start_date (str, optional): The start date for range filtering (inclusive).
    - end_date (str, optional): The end date for range filtering (inclusive).
    - specific_date (str, optional): A specific date to filter on.
    - last_n_days (int, optional): Filter the last N days.
    - date_range (tuple,optional): A tuple of (start_date, end_date) as an alternative to separate start/end parameters.
    - custom_filter (callable, optional):
        A custom function that takes a datetime object and returns True if the row should be included.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    # Ensure date_column is of a datetime type
    df[date_column] = pd.to_datetime(df[date_column])

    # Date range filtering
    if date_range:
        start_date, end_date = date_range
    if start_date:
        start_date = pd.to_datetime(start_date)
        df = df[df[date_column] >= start_date]
    if end_date:
        end_date = pd.to_datetime(end_date)
        df = df[df[date_column] <= end_date]

    # Specific date filtering
    if specific_date:
        specific_date = pd.to_datetime(specific_date)
        df = df[df[date_column] == specific_date]

    # Last N days filtering
    if last_n_days:
        cutoff_date = pd.to_datetime('today') - timedelta(days=last_n_days)
        df = df[df[date_column] >= cutoff_date]

    # Custom filter
    if custom_filter:
        df = df[df[date_column].apply(custom_filter)]

    return df


def filter_by_date2(df, date_columns, start_date=None, end_date=None, specific_date=None,
                   last_n_days=None, custom_filter=None):
    """
    Filters a DataFrame based on various date filtering criteria, supporting both single and multiple date columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter.
    - date_columns (str or list of str): The name(s) of the column(s) containing date information.
    - start_date (str, optional): The start date for range filtering (inclusive).
    - end_date (str, optional): The end date for range filtering (inclusive).
    - specific_date (str, optional): A specific date to filter on.
    - last_n_days (int, optional): Filter the last N days.
    - custom_filter (callable, optional): A custom function that takes a datetime object and returns True if the row should be included.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    if isinstance(date_columns, str):
        date_columns = [date_columns]  # Make it a list to simplify processing

    for date_column in date_columns:
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column])

            if start_date:
                df = df[df[date_column] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df[date_column] <= pd.to_datetime(end_date)]
            if specific_date:
                df = df[df[date_column] == pd.to_datetime(specific_date)]
            if last_n_days:
                cutoff_date = pd.to_datetime('today') - timedelta(days=last_n_days)
                df = df[df[date_column] >= cutoff_date]
            if custom_filter:
                df = df[df[date_column].apply(custom_filter)]

    return df

