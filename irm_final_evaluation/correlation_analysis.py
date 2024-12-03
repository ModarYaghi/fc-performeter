"""
A module for analyzing correlations in datasets.

This module provides a class `CorrelationAnalyzer` for:
- Calculating correlation matrices (Pearson, Spearman, Kendall Tau).
- Calculating p-values for statistical significance.
- Visualizing correlation matrices as heatmaps.
- Handling missing values in datasets.

"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr, kendalltau


class CorrelationAnalyzer:
    """
    A class for performing correlation analysis on a dataset.

    Features:
    - Calculate correlation matrices (Pearson, Spearman, Kendall Tau).
    - Compute p-values for variable correlations.
    - Visualize correlation matrices using heatmaps.
    - Clean datasets by handling missing values and dropping irrelevant columns.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the CorrelationAnalyzer with a dataset.

        Parameters:
        ----------
        data : pd.DataFrame
            The dataset to analyze.
        """
        self.data = data
        self.corr_matrix = None

    def clean_data(self, drop_columns=None, fill_method="mean"):
        """
        Cleans the dataset by dropping specified columns and handling missing values.

        Parameters:
        ----------
        drop_columns : list, optional
            List of column names to drop. Default is None.
        fill_method : str, optional
            Method to fill missing values. Options: 'mean', 'median', 'mode'. Default is 'mean'.
        """
        if drop_columns:
            self.data = self.data.drop(columns=drop_columns, errors="ignore")

        if fill_method == "mean":
            self.data = self.data.fillna(self.data.mean())
        elif fill_method == "median":
            self.data = self.data.fillna(self.data.median())
        elif fill_method == "mode":
            self.data = self.data.fillna(self.data.mode().iloc[0])
        else:
            raise ValueError("Invalid fill_method. Choose 'mean', 'median', or 'mode'.")

    def calculate_correlation(self, method="pearson"):
        """
        Calculates the correlation matrix using the specified method.

        Parameters:
        ----------
        method : str, optional
            Correlation method to use ('pearson', 'spearman', 'kendall'). Default is 'pearson'.

        Returns:
        -------
        pd.DataFrame
            The calculated correlation matrix.
        """
        if method not in ["pearson", "spearman", "kendall"]:
            raise ValueError(
                "Invalid method. Choose 'pearson', 'spearman', or 'kendall'."
            )
        self.corr_matrix = self.data.corr(method=method)
        return self.corr_matrix

    def compute_p_value(self, x, y, method="pearson"):
        """
        Computes the p-value for the correlation between two variables.

        Parameters:
        ----------
        x : pd.Series
            First variable (column) in the dataset.
        y : pd.Series
            Second variable (column) in the dataset.
        method : str, optional
            Correlation method to use ('pearson', 'spearman', 'kendall'). Default is 'pearson'.

        Returns:
        -------
        float
            The p-value for the correlation.
        """
        corr_func = {
            "pearson": pearsonr,
            "spearman": spearmanr,
            "kendall": kendalltau,
        }.get(method)
        if not corr_func:
            raise ValueError(
                "Invalid method. Choose 'pearson', 'spearman', or 'kendall'."
            )
        return corr_func(x, y)[1]

    def calculate_p_values(self, method="pearson"):
        """
        Calculates p-values for all variable pairs in the dataset.

        Parameters:
        ----------
        method : str, optional
            Correlation method to use ('pearson', 'spearman', 'kendall'). Default is 'pearson'.

        Returns:
        -------
        pd.DataFrame
            A matrix of p-values corresponding to the correlation matrix.
        """
        if method not in ["pearson", "spearman", "kendall"]:
            raise ValueError(
                "Invalid method. Choose 'pearson', 'spearman', or 'kendall'."
            )

        p_values = pd.DataFrame(
            np.zeros((self.data.shape[1], self.data.shape[1])),
            columns=self.data.columns,
            index=self.data.columns,
        )

        for i in self.data.columns:
            for j in self.data.columns:
                if i == j:
                    p_values.loc[i, j] = 0.0
                else:
                    try:
                        p_values.loc[i, j] = self.compute_p_value(
                            self.data[i], self.data[j], method
                        )
                    except (TypeError, ValueError) as e:
                        p_values.loc[i, j] = np.nan  # Mark invalid pairs as Nan
                        print(
                            f"Warning: Could not calculate p-value for {i} and {j}. Error: {e}"
                        )
        return p_values

    def visualize_heatmap(
        self, annotate=True, cmap="coolwarm", title="Correlation Matrix"
    ):
        """
        Visualizes the correlation matrix as a heatmap.

        Parameters:
        ----------
        annotate : bool, optional
            Whether to annotate the heatmap with values. Default is True.
        cmap : str, optional
            Colormap to use for the heatmap. Default is 'coolwarm'.
        title : str, optional
            Title of the heatmap. Default is 'Correlation Matrix'.
        """
        if self.corr_matrix is None:
            raise ValueError(
                "Correlation matrix not computed. Run 'calculate_correlation()' first."
            )

        plt.figure(figsize=(10, 8))
        sns.heatmap(self.corr_matrix, annot=annotate, cmap=cmap, fmt=".2f", cbar=True)
        plt.title(title)
        plt.show()

    def get_top_correlations(self, n=10):
        """
        Identifies the top n correlations in the dataset.

        Parameters:
        ----------
        n : int, optional
            Number of top correlations to return. Default is 10.

        Returns:
        -------
        pd.DataFrame
            A DataFrame of the top n correlations.
        """
        if self.corr_matrix is None:
            raise ValueError(
                "Correlation matrix not computed. Run 'calculate_correlation()' first."
            )

        corr_unstacked = self.corr_matrix.abs().unstack()
        sorted_corrs = corr_unstacked.sort_values(ascending=False)
        top_corrs = sorted_corrs[sorted_corrs < 1].drop_duplicates().head(n)
        return top_corrs

    def run_full_analysis(
        self, drop_columns=None, fill_method="mean", method="pearson", visualize=False
    ):
        """
        Runs the full analysis: cleans data, calculates correlations, and optionally visualizes.

        Parameters:
        ----------
        drop_columns : list, optional
            List of columns to drop. Default is None.
        fill_method : str, optional
            Method to fill missing values. Options: 'mean', 'median', 'mode'. Default is 'mean'.
        method : str, optional
            Correlation method to use ('pearson', 'spearman', 'kendall'). Default is 'pearson'.
        visualize : bool, optional
            Whether to visualize the correlation matrix. Default is False.

        Returns:
        -------
        pd.DataFrame
            The calculated correlation matrix.
        """
        self.clean_data(drop_columns, fill_method)
        self.calculate_correlation(method)
        if visualize:
            self.visualize_heatmap()
        return self.corr_matrix
