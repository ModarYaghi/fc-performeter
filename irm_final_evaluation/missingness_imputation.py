"""
Missing data imputation
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.utils import resample

# Load the data
data = pd.read_csv("datasets/re_rel_en_ds.csv")
# print(df.info())

# === Mode Imputation for Minimal Missingness ===
NETWORK_SIZE = "network_size"
mode_value = data[NETWORK_SIZE].mode()[0]
# print(mode_value)

# Fill missing values with the mode
data[NETWORK_SIZE] = data[NETWORK_SIZE].fillna(mode_value)  # type: ignore
print(f"Mode Imputation completed for '{NETWORK_SIZE}'.")
# print(df.info())


# === Predictive Imputation for Moderate Missingness === #
def predictive_imputation(df, target_column, predictors, hyperparam_tuning=True):
    """
    Perform predictive imputation for a target column with missing values using Random Forest.
    Args:
        df (DataFrame): The input data frame.
        target_column (str): The column with missing values to impute.
        predictors (list): List of predictor column names.
        hyperparam_tuning (bool): If True, perform hyperparameter tuning using GridSearchCV.

    Retruns:
        DataFrame: Data frame with imputed values for the target column.
    """
    print(f"Starting predictive imputation for '{target_column}'...")

    # STep 1: Prepare the data
    # Filter out rows where predictors or target are missing
    complete_data = df.dropna(subset=predictors + [target_column])
    if complete_data.empty:
        print(f"No complete rows available for predictors: {predictors}")
        return df

    # Handle class imbalance with oversampling
    majority_class = complete_data[target_column].value_counts().idxmax()
    majority_size = complete_data[target_column].value_counts().max()

    resampled_data = pd.concat(
        [
            resample(
                complete_data[complete_data[target_column] == cls],
                replace=True,
                n_samples=majority_size,
                random_state=42,
            )
            for cls in complete_data[target_column].unique()
        ]
    )

    # Shuffle resampled data
    resampled_data = resampled_data.sample(frac=1, random_state=42)

    # Define predictors (x) and target (y)
    x = resampled_data[predictors]
    y = resampled_data[target_column]

    # Step 2: Train-test split to evaluate the model
    # Train-test split to evaluate model (optional but recommended)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # Step 3: Initiatlize RAndom Forest model
    rf = RandomForestClassifier(random_state=42, class_weight="balanced")

    # Step 4: Hyperparameter Tuning (if endabled)
    if hyperparam_tuning:
        print("performing hyperparameter tuning...")
        param_grid = {
            "n_estimators": [50, 100],
            "max_depth": [None, 10],
            "min_samples_split": [2, 5],
        }

        grid_search = GridSearchCV(
            estimator=rf, param_grid=param_grid, cv=3, scoring="accuracy", verbose=1
        )
        grid_search.fit(x_train, y_train)

        # Use the best model from Grid Search
        rf = grid_search.best_estimator_
        print(f"Best Parameters: {grid_search.best_params_}")
    else:
        # Train with default Parameters
        rf.fit(x_train, y_train)

    # Step 5: Evaluate model performance
    y_pred = rf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy for '{target_column}': {accuracy:.2f}")

    # Step 6: Predict missing values
    missing_data = df[df[target_column].isnull()]
    if not missing_data.empty:
        x_missing = missing_data[predictors]
        predicted_values = rf.predict(x_missing)
        df.loc[df[target_column].isnull(), target_column] = predicted_values
        print(f"Imputed missing values for '{target_column}'.")
    else:
        print(f"No missing values to impute for '{target_column}'.")

    return df


# === Apply Predictive Imputation === #
PREDICTORS = [
    "qual_life12",
    "qual_life18",
]

# Impute missing values for "To what extent do you currently
# feel financially able to support and provide for your family? | relative_support2"
TARGET = "relative_support2"
data = predictive_imputation(
    df=data, target_column=TARGET, predictors=PREDICTORS, hyperparam_tuning=True
)

# === Verify Missingness Has Been Addressed === #
print("Final summary of missing values:")
print(data.isnull().sum())


# === Save the Cleaned Data === #
OUTPUT = "imputed_questionnaire_data.csv"
data.to_csv(OUTPUT, index=False)
print(f"Cleaned data saved to '{OUTPUT}'.")
