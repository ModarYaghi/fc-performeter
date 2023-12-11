from pydantic import BaseModel
from typing import List, Dict
import toml

# Define Pydantic models for each section


class DataType(BaseModel):
    btype: str
    ctype: str
    dtype: str
    itype: str
    stype: str


class PssSheet(BaseModel):
    screening: str
    intake: str
    group_counseling: str
    individual_counseling: str
    follow_up: str
    pei: str
    trw: str
    td: str
    cws: str
    aws: str


class PtSheet(BaseModel):
    psfs: str
    pt_int: str
    pt_group: str
    pt_individual: str
    pt_follow_up: str


class TrackerTdSheet(BaseModel):
    td_tracker: str


class SheetsNames(BaseModel):
    pss: PssSheet
    pt: PtSheet
    tracker_td: TrackerTdSheet


class DataSource(BaseModel):
    service: str
    sp: str
    name: str
    file: str
    password: str


class Variable(BaseModel):
    var: str
    type: str
    level: int


class Dataset(BaseModel):
    dataset: str
    variables: List[Variable]


class Config(BaseModel):
    data_types: DataType
    sheets_names: SheetsNames
    data_source: List[DataSource]
    datasets: List[Dataset]


def load_toml_data(file_path: str) -> Config:
    with open(file_path, "r") as file:
        data = toml.load(file)
    return Config(**data)


# Usage Example
config = load_toml_data("../config/config.toml")

# data_type = [i[1] for i in config.data_types]

datasets = config.datasets.variables

print(datasets)
