import inspect
import hashlib
from typing import Dict, Any, Callable

from ._os import create_dir_if_not_exists

HIDDEN_DIR = ".mlog"


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


def hash_name(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def _settings():
    create_dir_if_not_exists(HIDDEN_DIR)
