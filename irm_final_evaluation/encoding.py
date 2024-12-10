"""Encoding IRM Final Evaluation Survey Data"""

import logging

import pandas as pd

# Set logging for progress tracking
logging.basicConfig(level=logging.INFO)

pd.set_option("display.max_rows", None)  # Set to None to display all rows
pd.set_option("display.max_columns", None)  # Set to None to display all columns
# pd.set_option('display.width', 1000) # Increase width of the output.

# Step 1: Load the dataset and the codebook
dataset = pd.read_excel("cleaned_dataset.xlsx")
codebook = pd.read_excel("codebook.xlsx")

# Step 2: Filter relevant questions from the codebook
relevant_questions = codebook[codebook["relevance"] == 1]

# Step 3: Dynamically extract relevant numeric columns
code_columns = [col for col in relevant_questions.columns if col.isdigit()]
# print(code_columns)

# Step 3.1: Clean up whitespace for relevant rows and numeric columns
relevant_questions = relevant_questions.copy()
for code_col in code_columns:
    if code_col in relevant_questions.columns:
        relevant_questions[code_col] = (
            pd.Series(relevant_questions[code_col]).astype(str).map(str.strip)
        )


# Step 4: Iterate over the relevant questions and encode dataset columns
for _, row in relevant_questions.iterrows():
    column_name = row["question"]  # Get the corresponding column name in the dataset
    if column_name in dataset.columns:  # Only process if column exists
        logging.info("Encoding column %s", column_name)

    # Create a mapping dictionary by iterating ove the codebook columns
    mapping_dict = {
        row[code_col]: code_col
        for code_col in code_columns
        if code_col in row.index and not pd.isna(row.at[code_col])
    }

    # Replace values in the dataset column based on mapping
    dataset[column_name] = dataset[column_name].replace(mapping_dict)

    # Replace missing values (NaN) in the dataset column with a placeholder
    dataset[column_name] = dataset[column_name].fillna("NaN")

encoded_dataset = dataset
encoded_dataset.to_clipboard(index=False)
# encoded_dataset.to_csv("encoded_dataset.csv", index=False)
