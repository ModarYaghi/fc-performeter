import sys
import os

scritp_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(scritp_dir)
sys.path.append(parent_dir)

from src.data_reader import JSONDataReader

config_file_path = r"config/config.json"

config = JSONDataReader(config_file_path)
section = config.get_section("data_source")

for i in section:
    print(i)