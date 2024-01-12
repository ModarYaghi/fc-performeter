import pandas as pd

data = {
    "cat": ["A", "B", "A", "B"],
    "val": [10, 20, 30, 40],
}

df = pd.DataFrame(data)
print(df)
grouped = df.groupby("cat").sum()

print(grouped)
