import yaml
import toml
import json
from typing import Any


def replace_value_in_dict(obj: dict, old_value: Any, new_value: Any) -> int:
    """
    Recursively searches through a dictionary and replaces an old value with a new value.

    Parameters:
    obj (dict): The dictionary to search through.
    old_value (Any): The value to be replaced.
    new_value (Any): The value to replace with.

    Returns:
    int: The number of replacements made.
    """
    replacements = 0
    for k, v in obj.items():
        if isinstance(v, dict):
            replacements += replace_value_in_dict(v, old_value, new_value)
        elif v == old_value:
            obj[k] = new_value
            replacements += 1
    return replacements


def replace_and_write_to_yaml_file(
    file_path: str, old_value: Any, new_value: Any
) -> int:
    """
    Replaces all occurrences of a specific value with another value in a given YAML file.

    Parameters:
    file_path (str): The path to the YAML file.
    old_value (Any): The value to be replaced.
    new_value (Any): The value to replace with.

    Returns:
    int: The number of replacements made.
    """
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        replacements = replace_value_in_dict(data, old_value, new_value)

        if replacements > 0:
            with open(file_path, "w") as file:
                yaml.safe_dump(data, file, default_flow_style=False)

        return replacements

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return 0
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML file: {exc}")
        return 0
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return 0


def convert_yaml_to_other(yaml_file_path, file_path):
    with open(yaml_file_path, "r") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    if file_path.endswith(".toml"):
        with open(file_path, "w") as toml_file:
            toml.dump(yaml_data, toml_file)
    elif file_path.endswith(".json"):
        with open(file_path, "w") as json_file:
            json.dump(yaml_data, json_file, indent=4)


# convert_yaml_to_other(r"../config/config.yaml", r"../config/config.toml")
convert_yaml_to_other(r"../config/config.yaml", r"../config/config.json")
