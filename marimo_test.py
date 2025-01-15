import marimo

__generated_with = "0.10.12"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    import numpy as np
    from src.all_in_one import *
    """,
    name="_"
)


@app.cell
def _(np):
    x = np.arange(0, 101, 9)
    np.sin(x)
    return (x,)


if __name__ == "__main__":
    app.run()
