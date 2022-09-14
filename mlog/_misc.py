import inspect
from typing import Callable


def _is_method(func: Callable):
    spec = inspect.signature(func)
    if len(spec.parameters) > 0:
        if list(spec.parameters.keys())[0] in ("cls", 'self'):
            return True
    return False
