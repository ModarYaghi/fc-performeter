"""
Missing data imputation
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Load the data
data = pd.read_csv("datasets/re_rel_en_ds.csv")
# print(df.info())

# === Mode Imputation for Minimal Missingness ===
NETWORK_SIZE = "network_size"
mode_value = data[NETWORK_SIZE].mode()[0]
# print(mode_value)

# Fill missing values with the mode
data[NETWORK_SIZE] = data[NETWORK_SIZE].fillna(mode_value)
print(f"Mode Imputation completed for '{NETWORK_SIZE}'.")
# print(df.info())


# === Predictive Imputation for Moderate Missingness === #
def predictive_imputation(df, target_column, predictors):
    """
    Perform predictive imputation for a given target column using related predictors.
    Args:
        df (DataFrame): The input data frame.
        target_column (str): The column with missing values to impute.
        predictors (list): List of predictor column names.
    Retruns:
        DataFrame: Data frame with imputed values for the target column.
    """
    print(f"Starting predictive imputation for '{target_column}'...")

    # Filter rows where predictors and target are not missing
    complete_data = df.dropna(subset=predictors + [target_column])
    if complete_data.empty:
        print(f"No complete rows available for predictors: {predictors}")
        return df

    # Define X (predictors) and y (target)
    x = complete_data[predictors]
    y = complete_data[target_column]

    # Train-test split to evaluate model (optional but recommended)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # Train the Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(x_train, y_train)

    # Evaluate the model (option)
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy for '{target_column}': {accuracy: .2f}")

    # Impute missing values in the target column
    missing_data = df[df[target_column].isnull()]
    if not missing_data.empty:
        x_missing = missing_data[predictors]
        predicted_values = model.predict(x_missing)
        df.loc[df[target_column].isnull(), target_column] = predicted_values
        print(f"Imputation completed for '{target_column}'.")

    return df


# === Apply Predictive Imputation === #
PREDICTORS = [
    "qual_life12",
    "qual_life18",
]

# Impute missing values for "To what extent do you currently
# feel financially able to support and provide for your family? | relative_support2"
TARGET = "relative_support2"
data = predictive_imputation(df=data, target_column=TARGET, predictors=PREDICTORS)

# === Verify Missingness Has Been Addressed === #
print("Final summary of missing values:")
print(data.isnull().sum())


# === Save the Cleaned Data === #
OUTPUT = "imputed_questionnaire_data.csv"
data.to_csv(OUTPUT, index=False)
print(f"Cleaned data saved to '{OUTPUT}'.")
