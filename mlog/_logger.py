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
from ._exceptions import ArgumentNotCallable, ModeError


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """

    HIDDEN_DIR = ".mlog"

    def __init__(
        self,
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
    ) -> None:
        # TODO: Update type param for level
        logging.basicConfig(format=format, level=level)
        self.logger = logging.getLogger(__name__)

    # TODO: Divide the log by level into multiple logs if wanted
    # def add(self, key: str) -> None:
    #     # Add more output files
    #     # val = getattr(self, key)
    #     pass

    def log(
        self,
        func: Optional[Callable] = None,
        *,
        message: str = "",
        monitor_input: bool = True,
        monitor_output: bool = True,
        mode: Literal["info", "warning", "error"] = "info",
    ) -> Callable:
        """TODO:
        - Add possible options that should be appended to the log
        - Concat combination into message
        - Add index => unique id
        - Related to ML
        - Event based calculations of input / output
        - Save to hidden directory
        """
        if mode not in ("info", "warning", "error"):
            raise ModeError(
                f"{mode} is not a possible mode. Please choose among ['info', 'warning', 'error']"
            )
        log = getattr(self, mode)

        def wrapper(func: Callable, *args, **kwargs):
            log(message + str(args))
            if _is_method(func):
                return func(self, *args, **kwargs)
            return func(*args, **kwargs)

        if func is not None:
            if not callable(func):
                raise ArgumentNotCallable(
                    "Not a callable. Did you use a non-keyword argument?"
                )
            return wraps(func)(partial(wrapper, func))

        def wrap_callable(func: Callable) -> Callable:
            return wraps(func)(partial(wrapper, func))

        return wrap_callable

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)
