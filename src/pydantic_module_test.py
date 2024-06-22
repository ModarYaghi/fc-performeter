from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict
import yaml


class User(BaseModel):
    id: int
    name: str
    email: str


# Parsing JSON to a Python object
json_data = '{"id": 1, "name": "John Doe", "email": "john@example.com"}'
user = User.parse_raw(json_data)
print(user)


# Serializing Python object to JSON
# user_json = user.josn()
# print(user_json)
