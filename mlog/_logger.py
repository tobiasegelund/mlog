import json
import logging

from ._os import find_hidden_mlog_dir
from ._states import LogInput, LogOutput, LogProfile


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    Typestates: logger.profile.log(), logger.ml.log(), logger.data.log()

    # What to do if we observe the same name twice? Link it based on the script it is found in?
     - Options to hard reset at each load, or at each 10 run then clear cache etc.
     - Perhaps include environment variable
     - Logging folders / files and by levels
     - Add RWLock to read and write cache files, may be proper use of from contextlib import contextmanager
    """

    _hidden_dir = find_hidden_mlog_dir()

    def __init__(
        self,
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
    ) -> None:
        # TODO: Update type param for level
        logging.basicConfig(format=format, level=level)
        self.logger = logging.getLogger(__name__)

        # Initialize the possible states
        # TODO: Apply logic to each state here. In case a certain connection or file must be written for input logs
        self._profile = LogProfile(self)
        self._input = LogInput(self)
        self._output = LogOutput(self)

    @property
    def profile(self) -> LogProfile:
        # Specify requirements to log profiling, e.g. define the min/max to execute the job
        # The amount of data
        return self._profile

    @property
    def input(self) -> LogInput:
        return self._input

    @property
    def output(self) -> LogOutput:
        # Thresholds
        return self._output

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)
