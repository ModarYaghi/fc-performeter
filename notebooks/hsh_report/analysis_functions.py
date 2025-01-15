import pandas as pd


def normalized_value_counts(series):
    counts = series.value_counts(dropna=False)
    percentages = (
        series.value_counts(normalize=True, dropna=False).mul(100).round(2).astype(str)
        + "%"
    )
    # result = pd.concat([counts, percentages], axis=1, keys=['N', '%'])
    result = pd.DataFrame({"N": counts, "%": percentages})
    return result


if __name__ == "__main__":
    # Code to run when this module is executed directly goes here
    # For now, it's just a placeholder
    pass
