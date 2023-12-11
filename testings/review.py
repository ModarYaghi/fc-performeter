from src.data_reader import JSONDataReader

config_file_path = r"../config/config.json"


config = JSONDataReader(config_file_path)

todo = config.get_files_by_scope("pt")

print(todo)
