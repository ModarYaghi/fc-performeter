""" "
A function to convert categorical variables into dummy/indicator variables.
The function needs id and categorical variable to work.
The function also aggregates the dummy variables into a single row for each id.
"""

import pandas as pd


def dumm_aggr(df, id_column, categorical_column):
    # Check for duplicates in 'id' and need combination
    duplicate_check = df.duplicated(subset=[id_column, categorical_column], keep=False)
    if duplicate_check.any():
        raise ValueError("There are duplicate entries for the same 'id' and 'cat_col'.")

    # Step 2: One-Hot Encode the 'cat_col'
    dummies = pd.get_dummies(df[categorical_column])

    # Step 3: concatenate the dummies with the original dataframe
    df_with_dummies = pd.concat([df, dummies])

    # Step 4: Group by the id column and aggregate using 'max' for dummy columns,
    # while keeping the first occurrence of other columns
    non_dummy_columns = [col for col in df.columns if col not in [categorical_column]]
    aggregated_df = df_with_dummies.groupby(id_column, as_index=False).agg(
        {
            col: "first" if col in non_dummy_columns else "max"
            for col in df_with_dummies.columns
        }
    )

    return aggregated_df
