import datetime
from pathlib import Path
import logging
from typing import Union, Optional

from ._os import find_hidden_mlog_dir
from ._utils import hash_string
from ._states import LogInput, LogOutput, LogProfile


class Logger:
    """A high-level extension of the logger class from Python standard logging library.

    On one hand the class holds the same features and settings as the standard library, while on the other
    it has extended it options to calculate metrics of input and output of functions and methods.

    The logging class is focused around machine learning systems, and to monitor any changes in input and output data
    to catch any data shifts.

    Params:


    Usage:
        >>> from mlog import Logger
        >>> logger = Logger()

    Typestates: logger.profile.log(), logger.ml.log(), logger.data.log()

    # What to do if we observe the same name twice? Link it based on the script it is found in?
     - Perhaps include environment variable
     - Logging folders / files and by levels
    """

    # _hidden_dir = find_hidden_mlog_dir()

    def __init__(
        self,
        *,
        filename: Optional[Union[str, Path]] = None,
        filemode: str = "a",
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        run_id: Optional[str] = None,
    ) -> None:
        logging.basicConfig(
            filename=filename, filemode=filemode, format=format, level=level
        )
        self.logger = logging.getLogger(__name__)

        # Initialize the possible states
        # TODO: Apply logic to each state here. In case a certain connection or file must be written for input logs
        run_id = self._create_run_id(run_id=run_id)
        self._profile = LogProfile(self, run_id=run_id)
        self._input = LogInput(self, run_id=run_id)
        self._output = LogOutput(self, run_id=run_id)

    def _create_run_id(self, run_id: Optional[str] = None) -> str:
        if run_id is None:
            return hash_string(str(datetime.datetime.now()), length=6)
        return run_id

    @property
    def profile(self) -> LogProfile:
        # Specify requirements to log profiling, e.g. define the min/max to execute the job
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
