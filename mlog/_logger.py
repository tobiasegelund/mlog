# import time
# import datetime
import logging
# from types import FunctionType
from typing import Callable, Literal

from ._misc import _is_method
# from ._tracing import Tracing
# from ._profiling import Profiling


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """
    def __init__(self, format: str = "%(asctime)s | %(message)s", level = logging.INFO) -> None:
        logging.basicConfig(format=format, level=level)
        self.logger = logging.getLogger(__name__)

    def add(self, key: str) -> None:
        # Add more output files
        # val = getattr(self, key)
        pass

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

    def log(self, *, mode: Literal["debug", "info"] = "debug"):
        def wrapper(func):
            if isinstance(func, Callable):
                if _is_method(func):
                    def inner(self, *args, **kwargs):
                        return func(self)
                    return inner
                else:
                    def inner(*args, **kwargs):
                        return func()
                    return inner
            else:
                raise ValueError()
        return wrapper

    def debug(self, msg: str) -> None:
        logging.debug(msg)

    def info(self, msg: str) -> None:
        logging.info(msg)

    def warning(self, msg: str) -> None:
        logging.warning(msg)

    def error(self, msg: str) -> None:
        logging.error(msg)

    def profile(self) -> None:
        pass
        # activate / deactivate

    def trace(self) -> None:
        pass
