from src.config_reader import YAMLConfigReader


class Dataset:
    """Interface for a dataset."""

    def __init__(self, config_path: str, sheet_name: str):
        # Initialize the dataset.
        self.config_path = config_path
        self.sheet_name = sheet_name

        # Load the dataset configuration.
        self.config = YAMLConfigReader(self.config_path)

        # Get the variable names for the dataset.
        self.vars = self.config.get_variable_names_by_dataset(self.sheet_name)

        # Get the variable names for the dataset at level 0.
        self.bvars = self.config.get_variable_names_by_dataset_and_level(
            self.sheet_name, 0
        )

        # Get the variable names for the dataset of type datetime64[ns].
        self.dvars = self.config.get_variable_names_by_dataset_and_type(
            self.sheet_name, "datetime64[ns]"
        )

        # Get the variable names for the dataset of type Int64.
        self.ivars = self.config.get_variable_names_by_dataset_and_type(
            self.sheet_name, "Int64"
        )

        self.svars = self.config.get_variable_names_by_dataset_and_type(
            self.sheet_name, "StringDtype"
        )

        self.cvars = self.config.get_variable_names_by_dataset_and_type(
            self.sheet_name, "category"
        )

        self.bovars = self.config.get_variable_names_by_dataset_and_type(
            self.sheet_name, "boolean"
        )


# if __name__ == "__main__":
# dataset = Dataset(config_file, "IPT")
# print(dataset.vars)
# print(len(dataset.vars))
