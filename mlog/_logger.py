import datetime
from pathlib import Path
import logging
from typing import Union, Optional, Literal

from ._os import find_hidden_mlog_dir
from ._utils import hash_string
from ._states import LogInput, LogOutput, LogProfile


class Logger:
    """A high-level extension of the logger class from Python standard logging library.

    The class stores most of the same features as the standard library's logging class,
    but with an extension of decorator to to calculate metrics on input and output of functions and methods.

    Its focus is on machine learning systems, in order to log and monitor changes in input and output data
    of functions to catch data shifts before its too late.

    Params:
        filename, [str, Path], default=None: The filepath to store logging output.
        filemode, str, default='a': Use 'w' to overwrite the file or 'a' to append to the file.
        format, str, default="%(asctime)s | %(levelname)s | %(message)s": Please check out Python's
            logging library for more information on formatting.
        level, logging.LEVEL, default=logging.INFO: Please check out Python's logging library
            for more information on level.
        run_id, str, default=None: Optional to choose a run id, if none, a hash value will be
            used
        verbose, bool, default=True: Verbose output of logging, including run id and file path to
            function

    Usage:
        >>> from mlog import Logger
        >>> logger = Logger()

        State: Profile
        >>> @logger.profile.log(execution_time=True, memory_usage=True)
        >>> def func(df):
        >>>    pass

        State: Input
        >>> @logger.input.log(metrics={"df": ["mean"]})
        >>> def func(df):
        >>>    pass

        >>> @logger.input.log(metrics={"df": {"feat1": {"mean": (4, 6)}}})
        >>> def func(df):
        >>>    pass

        >>> @logger.input.log(metrics={"X": {0: {"mean": (4, 6)}}})
        >>> def func(df):
        >>>    pass

        >>> @logger.input.log(metrics={"X": {0: ["mean"]}})
        >>> def func(df):
        >>>    pass

        State: Output
        >>> logger.output.log(metrics={"mean": (0.5, 0.8), "percentile10": None})
        >>> def func(X):
        >>>     return X

        >>> logger.output.log(metrics=["mean", "percentile1"])
        >>> def func(X):
        >>>     return X

    The decorators can also be combined to track both input, output and profile of a function
    """

    # _hidden_dir = find_hidden_mlog_dir()

    def __init__(
        self,
        *,
        filename: Optional[Union[str, Path]] = None,
        filemode: Literal["a", "w"] = "a",
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        run_id: Optional[str] = None,
        verbose: bool = True,
    ) -> None:
        logging.basicConfig(
            filename=filename, filemode=filemode, format=format, level=level
        )
        self.logger = logging.getLogger(__name__)

        # Initialize the possible states
        # TODO: Apply logic to each state here. In case a certain connection or file must be written for input logs
        run_id = self._create_run_id(run_id=run_id)
        self._profile = LogProfile(self, run_id=run_id, verbose=verbose)
        self._input = LogInput(self, run_id=run_id, verbose=verbose)
        self._output = LogOutput(self, run_id=run_id, verbose=verbose)

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
