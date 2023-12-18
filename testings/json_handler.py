import json
from typing import List, Dict, Optional


class Variable:
    def __init__(self, name: str, type: str, level: str):
        """Initialize a Variable with a name, type, and level."""
        self.name = name
        self.type = type
        self.level = level


class Dataset:
    def __init__(self, name: str, variables: List[Variable]):
        """Initialize a Dataset with a name and a list of Variables."""
        self.name = name
        self.variables = variables

    def filter_variables(
        self, var_type: Optional[str] = None, var_level: Optional[str] = None
    ) -> List[Variable]:
        """Filter the variables in the Dataset based on type and level."""
        return [
            var
            for var in self.variables
            if (var_type is None or var.type == var_type)
            and (var_level is None or var.level == var_level)
        ]


class JSONDataHandler:
    def __init__(self, file_path: str):
        """Initialize the JSONDataHandler with a file path."""
        self.data = self.load_json(file_path)
        self.datasets = self.create_datasets()

    def load_json(self, file_path: str) -> Dict:
        """Load JSON data from a file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"File {file_path} is not a valid JSON file.")
            return {}

    def get_sheets_names(self, category: str) -> List[str]:
        """Get the names of the sheets for a specific category."""
        return self.data["sheets_names"].get(category, [])

    def get_variable_details(self, variable_name: str) -> Optional[Dict]:
        """Get the details of a specific variable."""
        return self.data["variables"].get(variable_name, None)

    def get_dataset_variables(self, dataset_name: str) -> List[str]:
        """Get the variables of a specific dataset."""
        return self.data["datasets"].get(dataset_name, [])

    def search_variable_in_datasets(self, variable_name: str) -> List[str]:
        """Search for a variable in all datasets and return the datasets that contain it."""
        datasets_containing_var = []
        for dataset, vars in self.data["datasets"].items():
            if variable_name in vars:
                datasets_containing_var.append(dataset)
        return datasets_containing_var

    def create_datasets(self) -> Dict[str, Dataset]:
        """Create Dataset objects for all datasets in the data."""
        datasets = {}
        for dataset_name, var_names in self.data["datasets"].items():
            variables = [
                Variable(name, **self.data["variables"][name]) for name in var_names
            ]
            datasets[dataset_name] = Dataset(dataset_name, variables)
        return datasets

    def get_dataset(self, dataset_name: str) -> Optional[Dataset]:
        """Get a specific Dataset."""
        return self.datasets.get(dataset_name, None)
