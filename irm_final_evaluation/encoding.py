"""Encoding IRM Final Evaluation Survey Data"""

import pandas as pd

pd.set_option('display.max_rows', None)  # Set to None to display all rows
pd.set_option('display.max_columns', None)  # Set to None to display all columns
# pd.set_option('display.width', 1000) # Increase width of the output.

# Step 1: Load the dataset and the codebook
dataset = pd.read_excel('cleaned_dataset.xlsx')
codebook = pd.read_excel('codebook.xlsx')

# Step 2: Filter relevant questions from the codebook
relevant_questions = codebook[codebook['relevance'] == 1]

# Step 3: List of relevant columns in the codebook (based on your specified column names)
code_columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '666', '777', '888', '999', 'NaN']

# Trim whitespace for relevant rows and specific columns of interest
for code_col in code_columns:
    if code_col in relevant_questions:
        relevant_questions[code_col] = relevant_questions[code_col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
            )

# Step 4: Iterate over the relevant questions and encode dataset columns
for _, row in relevant_questions.iterrows():
    q_index = int(row['q_index'])  # Get the questions index to identify the dataset column
    column_name = row['question']  # Get the corresponding column name in the dataset

    # Create a mapping dictionary by iterating ove the codebook columns
    mapping_dict = {}
    for code_col in code_columns:
        # Check if the codebook column exists and has a value
        if code_col in row and pd.notna(row[code_col]):
            mapping_dict[row[code_col]] = code_col  # Create a mapping {vlaue: code_col}

    # Apply the mapping to ghe dataset column with the name corresponding to the question
    if column_name in dataset.columns:
        # Replace known values in the dataset using the mapping dictionary
        dataset[column_name] = dataset[column_name].replace(mapping_dict)

        # Replace empty cells (NaN) in the dataset column with the string 'NaN'
        dataset[column_name] = dataset[column_name].fillna('NaN')

encoded_dataset = dataset
encoded_dataset.to_clipboard(index=False)
