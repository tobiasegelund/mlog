"""
https://lemonfold.io/posts/2022/dbc/typed_decorator/
"""
# import time
# import datetime
import logging
# from types import FunctionType
from typing import Callable, Literal, Optional
from functools import wraps, partial

from ._misc import _is_method


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """
    level_mapping = {
        "debug": self.debug,
        "info": self.info,
        "warning": self.warning,
        "error": self.error,
    }


    def __init__(self, format: str = "%(asctime)s | %(message)s", level = logging.INFO) -> None:
        logging.basicConfig(format=format, level=level)
        self.logger = logging.getLogger(__name__)

    # TODO: Divide the log by level into multiple logs if wanted
    # def add(self, key: str) -> None:
    #     # Add more output files
    #     # val = getattr(self, key)
    #     pass

    # def log(self, func):
    #     if _is_method(func):
    #         def wrapper(self):
    #             return func(self)
    #         return wrapper

    #     elif isinstance(func, FunctionType):
    #         def wrapper(*args, **kwargs):
    #             return func()
    #         return wrapper
    #     else:
    #         raise ValueError()

    def log(self, func: Optional[Callable] = None,
            *,
            description: str = "",
            mode: Literal["debug", "info", "warning", "error"] = "debug") -> None:
        """TODO:
            - Add possible options that should be appended to the log
            - Concat combination into message
        """
        def wrapper(func: Callable):
            if _is_method(func):
                # @wraps(func)
                def inner(self, *args, **kwargs):
                    return func(self)
                return inner
            else:
                # @wraps(func)
                def inner(*args, **kwargs):
                    return func()
                return inner

        if func is not None:
            if not callable(func):
                raise ValueError("Not a callable. Did you use a non-keyword argument?")
            return wraps(func)(partial(wrapper, func))

        def decorator(func: Callable) -> Callable:
            return wraps(func)(partial(wrapper, func))

        return decorator

    def debug(self, msg: str) -> None:
        logging.debug(msg)

    def info(self, msg: str) -> None:
        logging.info(msg)

    def warning(self, msg: str) -> None:
        logging.warning(msg)

    def error(self, msg: str) -> None:
        logging.error(msg)
