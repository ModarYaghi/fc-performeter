import marimo

__generated_with = "0.10.13"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import sys
    from pathlib import Path
    import warnings

    warnings.simplefilter("ignore", UserWarning)
    return Path, pd, sys, warnings


@app.cell
def _():
    # import all_in_one as al
    # from analysis_functions import normalized_value_counts
    # from path_management import path_manager, Category, PSFile
    return


@app.cell
def _(pd):
    # To get rid of 0s that represent time in date columns.
    def date_corr(df, date_list_col):
        # a function for keep only date part
        for col in date_list_col:
           df[col] = pd.to_datetime(df[col]).dt.date  # keep only the date part
        return df
    return (date_corr,)


@app.cell
def _(pd):
    # Create Min-Max-Date DataFrame
    def minmax_date_df(df, date_list_col, id, service):
        # Ensure all date columns are datetime and replace NaN with a consistent value
        for col in date_list_col:
            df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert to datetime, error are set to NaT.
        new_df = pd.DataFrame()
        new_df[id] = df[id]
        new_df['min_date'] = df[date_list_col].min(axis=1, skipna=True).dt.normalize()
        new_df['max_date'] = df[date_list_col].max(axis=1, skipna=True).dt.normalize()
        new_df['service'] = service

        new_df = new_df[['min_date', 'max_date', 'service', id]]

        return new_df
    return (minmax_date_df,)


@app.cell
def _(date_corr, pd):
    scr = pd.read_csv(r"../../data/processed/1224/01_psscr_1224.csv")
    scr_date_col = ['sc_s1', 'pei_pre_as', 'sc_re']
    scr = date_corr(scr, scr_date_col)
    uq_scr = scr.drop_duplicates(subset='rid')
    return scr, scr_date_col, uq_scr


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""# Psychotherap""")
    return


@app.cell
def _(date_corr, pd):
    psint = pd.read_csv(r"../../data/processed/1224/02_psint_1224.csv")
    psint_date_col = ['nt_s1', 'nt_s2', 'nt_s3', 'nt_re']
    psint = date_corr(psint, psint_date_col)
    return psint, psint_date_col


@app.cell
def _(minmax_date_df, psint, psint_date_col):
    # Creating the Min and Max Date DataFrame
    mxpsint = minmax_date_df(psint, psint_date_col, 'rid', 'psint')
    return (mxpsint,)


@app.cell
def _(mxpsint):
    mxpsint
    return


if __name__ == "__main__":
    app.run()
