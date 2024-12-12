"""
Data Missingness
"""

import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

# == Quantify The Extent of Missing Data for Each Question ==

# Calculate Missing Data Percentages
df = pd.read_csv("re_rel_en_ds.csv")
check_df = df.iloc[:, 5:10]
# print(check_df)

# Count missing values for each column
missing_count = df.isnull().sum()
print(missing_count)

# Calculate missing value counts and percentages
missing_percentages = df.isnull().sum() / len(df) * 100

missing_summary = pd.DataFrame(
    {"Missing Count": missing_count, "Missing Percentage": missing_percentages}
).sort_values(by="Missing Percentage", ascending=False)

# missing_summary.to_clipboard()

# == Visualize the Missing Data ==

# === Plot Missing Data Percentages
missing_summary["Missing Percentage"].plot(
    kind="bar", figsize=(10, 6), title="Percentage of Missing Data per Column"
)
plt.xlabel("Columns")
plt.ylabel("Missing Percentage (%)")
# plt.show()

# === Visualize Missingness Across Rows
msno.matrix(df, figsize=(10, 6), fontsize=12)
# plt.show()

# == Investigate Patterns and Causes of Missingness

# ==== Missing by Groups
# To determine if specific groups are disproportionately affected, group the dataset by key variables
# and calculate the percentage of missing data for each group.
