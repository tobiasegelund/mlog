import inspect
import hashlib
from typing import Dict, Any, Callable, Optional, Union, Tuple, List

from ._os import create_dir_if_not_exists
from ._exceptions import DataTypeError

HIDDEN_DIR = ".mlog"


def _settings():
    create_dir_if_not_exists(HIDDEN_DIR)


def is_method(func: Callable):
    spec = inspect.signature(func)
    if len(spec.parameters) > 0:
        if list(spec.parameters.keys())[0] in ("cls", "self"):
            return True
    return False


def map_args(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """Return a dictionary of mapped args name and values (incl. kwargs)"""
    func_args = list(inspect.signature(func).parameters.keys())
    # TODO: A more dynamic method to filter out cls and self keywords
    if func_args[0] in ("cls", "self"):
        func_args = func_args[1:]
    args_length = len(args)
    return dict(zip(func_args[:args_length], args), **kwargs)


def hash_string(name: str, length: Optional[int] = None) -> str:
    if length is not None:
        return hashlib.md5(name.encode("utf-8")).hexdigest()[:length]
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def validate_dtype(input: Union[List, Tuple], expected_dtype: Any) -> None:
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


def unwrap(func):
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    return func
