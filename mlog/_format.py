"""
Format the output before write
"""
import json
from typing import Dict, Any


def marshalling_kwargs(**kwargs) -> str:
    _dict = {**kwargs}
    return marshalling_dict(_dict)


def marshalling_dict(dictionary: Dict[Any, Any]) -> str:
    return json.dumps(dictionary)
