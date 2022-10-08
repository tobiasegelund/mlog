"""
Format the output before write
"""
import json
from typing import Dict, Any, List, Tuple, Union
from ._exceptions import DataTypeError


def marshalling_kwargs(**kwargs) -> str:
    _dict = {**kwargs}
    return marshalling_dict(_dict)


def marshalling_dict(dictionary: Dict[Any, Any]) -> str:
    return json.dumps(dictionary)


def convert_bytes_to_mb(bytes: int) -> float:
    return bytes * 10**-6


def convert_bytes_to_gb(bytes: int) -> float:
    return bytes * 10**-9
