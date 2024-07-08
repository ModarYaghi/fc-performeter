import os
import sys
import json

script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

json_module = r'config/config.json'

# Load the original JSON data
with open(json_module, 'r') as file:
    original_data = json.load(file)

new_data = {
    "sheets_names": {},
    "variables": {},  # Will be populated with all variables
    "datasets": {}
}

# Transform sheets_names
for group, sheets in original_data["sheets_names"].items():
    new_data["sheets_names"][group] = list(sheets.values())

# Populate variables (assuming all are common)
for dataset in original_data["datasets"]:
    for var in dataset["variables"]:
        var_name = var["var"]
        if var_name not in new_data["variables"]:
            new_data["variables"][var_name] = {"type": var["type"], "level": var["level"]}

# Transform datasets
for dataset in original_data["datasets"]:
    dataset_name = dataset["dataset"]
    new_data["datasets"][dataset_name] = [var["var"] for var in dataset["variables"]]

# Write the new JSON data to a file
with open(r'config/transformed_data.json', 'w') as file:
    json.dump(new_data, file, indent=4)