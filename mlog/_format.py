"""
Format the output before write
"""
from typing import Dict, Any


def marshalling(**kwargs) -> Dict[str, Any]:
    return {key: val for key, val in kwargs}
