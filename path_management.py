import os


# Get the environment variable of the project - fc-performeter
root = os.getenv(
    "FcPerformeter"
)  # TODO : set the environment variable for the project in the OFFICE


# Main directories in use
config, config_yaml = "config", "config.yaml"
data = "data"
raw = "raw"
ps = "ps"
pt = "pt"
processed = "processed"

data_dir = "1223"

# path to config.yaml
config_file = os.path.join(root, config, config_yaml)

# path to raw data - xlsx files
ps_raw_data = os.path.join(root, data, raw, data_dir, ps)
pt_raw_data = os.path.join(root, data, raw, data_dir, pt)
processed_data = os.path.join(root, data, processed, data_dir)
