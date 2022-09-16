"""
Format the output before write
"""
import json
from typing import Dict, Any


def marshalling(**kwargs) -> str:
    return json.dumps(**kwargs)  # {key: val for key, val in kwargs}
