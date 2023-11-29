from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict
import yaml


# Define your Pydantic models
class DatasetVariable(BaseModel):
    var: str
    type: Optional[str] = None
    level: Optional[int] = None


class Dataset(BaseModel):
    dataset: str
    variables: List[DatasetVariable]


class DataSource(BaseModel):
    file: str
    password: Optional[str] = None
    service: Optional[str] = None


class YAMLData(BaseModel):
    data_source: List[DataSource] = []
    datasets: List[Dataset] = []

    @classmethod
    def load_from_file(cls, file_path: str):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return cls(**data)

    def get_file_password(self) -> Dict[str, str]:
        return {source.file: source.password for source in self.data_source}


# Usage
try:
    yaml_data = YAMLData.load_from_file(r"../static_data/config.yaml")
except ValidationError as e:
    print("Error loading YAML data:", e)


# for source in yaml_data.data_source:
#     print(source.file)
#     print(source.password)
#     print(source.service)

# passwords = yaml_data.get_file_password()
# print(passwords)

print(yaml_data.datasets)
