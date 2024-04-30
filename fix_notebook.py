import os

import nbformat
from nbformat.validator import validate, ValidationError


def fix_notebook(path):
    print(f"Opening notebook: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        # check if there's any need to fix based on 'execution_count'
        needs_fixing = any(cell.get("execution_count") is None for cell in notebook.cells if cell.cell_type == "code")

        if needs_fixing:
            print(f"Notebook {path} requires fixing.")
            used_execution_counts = set()
            for cell in notebook.cells:
                if cell.cell_type == "code" and cell.get("execution_count") is not None:
                    used_execution_counts.add(cell["execution_count"])

            for cell_index, cell in enumerate(notebook.cells):
                if cell.cell_type == "code" and (
                        cell.get("execution_count") is None or not isinstance(cell.get("execution_count"), int)):
                    cell["execution_count"] = max(used_execution_counts, default=0) + 1
                    used_execution_counts.add(cell["execution_count"])
                    print(f"Assigned new execution_count: {cell['execution_count']} to cell {cell_index}")

            with open(path, "w", encoding="utf-8") as f:
                nbformat.write(notebook, f)
            print(f"Fixed and saved notebook at {path}")
        else:
            print(f"Notebook {path} is valid and does not need fixing.")

    except ValidationError as e:
        print(f"Validation failed for {path}; {e}")


def fix_notebooks_in_directory(directory_path):
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith(".ipynb"):
                notebook_path = os.path.join(dirpath, filename)
                fix_notebook(notebook_path)
                # break


if __name__ == "__main__":
    fix_notebooks_in_directory("notebooks")
