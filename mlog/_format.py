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


def validate_dtype(input: Union[List[Any], Tuple[Any]], expected_dtype: Any) -> None:
    if isinstance(expected_dtype, list) or isinstance(expected_dtype, tuple):
        for i in input:
            check = list(isinstance(i, exp_t) for exp_t in expected_dtype)
            if not any(check):
                raise DataTypeError(
                    f"{type(i)} does not meet the expected data type {expected_dtype}"
                )
        return

    for i in input:
        if not isinstance(i, expected_dtype):
            raise DataTypeError(
                f"{type(i)} does not meet the expected data type {expected_dtype}"
            )
    return
