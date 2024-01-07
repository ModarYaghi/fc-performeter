from src.config_reader import YAMLConfigReader
from path_management import config_file


config = YAMLConfigReader(config_file)

print(config)
