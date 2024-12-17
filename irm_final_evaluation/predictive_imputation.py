"""
Predictive Imputation
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import tarin_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.utils import resample


class PredictiveImputer:
    def __init__(self, df, target_column, predictors):
        """
        Initialize the Predictive Imputer.

        Args:
            df (pd.DataFrame): The input data frame
            target_column (str): Column with missing values to impute.
            predictors (list of str): List of predictor columnm names.
        """
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not in the data frame.")
        if any(p not in df.columns for p in predictors):
            raise ValueError("One or more predicotrs are not in the data frame.")

        self.df = df.copy()
        self.target_column = target_column
        self.predictors = predictors
        self.model = RandomForestClassifier(random_state=42, class_weight="balanced")

    def _prepare_data(self):
        """
        Prepare the data for training, including resampling for class balance.

        Returns:
            pd.DataFrame, pd.Series: Resampled predictors and target.
        """
        complete_data = self.df.dropna(subset=self.predictors + [self.target_column])
        if complete_data.empty:
            raise ValueError(
                "No complete rows available for predictors and target column."
            )

        majority_size = complete_data[self.target_column].value_counts().max()

        resampled_data = pd.concat(
            [
                resample(
                    complete_data[complete_data[self.target_column] == cls],
                    replace=True,
                    n_samples=majority_size,
                    random_state=42,
                )
                for cls in complete_data[self.target_column].unique()
            ]
        ).sample(frac=1, random_state=42)  # Shuffle data

        x = resampled_data[self.predictors]
        y = resampled_data[self.target_column]
        return x, y

    def _train_model(self, x_train, y_train, hyperparam_tuning):
        """
        Train the Random Forest model with or sithout hyperparameter tuning.

        Args:
        x_train (pd.DataFrame): Training predictors.
        y_train (pd.Series): Training target.
        hyperparam_tuning (bool): Whether to perform hyperparameter tuning.

        Returns:
            RandomForestClassifier: Trained model.
        """
        if hyperparam_tuning:
            print("Performing hyperparameter tuning...")
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 5],
            }
            grid_search = GridSearchCV(
                estimatro=self.model,
                param_grid=param_grid,
                cv=3,
                scoring="accuracy",
                verbose=1,
            )
            grid_search.fit(x_train, y_train)
            print(f"Best Parameters: {grid_search.best_params_}")
            return grid_search.best_estimator_

        print("Training model with default parameters...")
        self.model.fit(x_train, y_train)
        return self.model

    def impute(self, hyperparam_tuning=True):
        """
        Perform predictive imputation for the target column.

        Args:
            hyperparam_tuning (bool): Whether to perform hyperparameter tuning.

        Returns:
            pd.DataFrame: Data frame with imputed values for the target column.
        """
        print(f"Strting predictive imputation for '{self.target_column}'...")

        try:
            x, y = self._prepare_data()
        except ValueError as e:
            print(e)
            return self.df

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        self.model = self._train_model(x_train, y_train, hyperparam_tuning)

        # Evaluate the model
        y_pred = self.model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy for '{self.target_column}': {accuracy: .2f}")

        # Impute missing values
        missing_data = self.df[self.df[self.target_column].isnull()]
        if not missing_data.empty:
            x_missing = missing_data[self.predictors]
            predicted_values = self.model.predict(x_missing)
            self.df.loc[self.df[self.target_column].isnull(), self.target_column] = (
                predicted_values
            )
            print(f"Imputed missing values for '{self.target_column}'.")

        else:
            print(f"No missing values to impute for '{self.target_column}'.")

        return self.df
