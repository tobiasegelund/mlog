import logging

from ._tracing import Tracing
from ._profiling import Profiling


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """
    # Default logger here - so writing is optional with classmethods
    def __init__(self) -> None:
        pass

    def add(self) -> None:
        pass

    @classmethod
    def debug(cls, msg: str) -> None:
        pass

    @classmethod
    def info(cls, msg: str) -> None:
        pass

    @classmethod
    def warning(cls, msg: str) -> None:
        pass

    @classmethod
    def error(cls, msg: str) -> None:
        pass
