import logging
from typing import Callable, Literal, Optional, Dict, List, Any
from functools import wraps, partial

import pandas as pd
import numpy as np

from ._misc import _is_method, map_args
from ._exceptions import ArgumentNotCallable, LevelError, InputFormatError
from ._metrics import DataMetrics
from ._format import marshalling_dict


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """

    def __init__(
        self,
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
        # environment: str = "development",
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
        input_metrics: Optional[Dict[str, List[str]]] = None,
        output_metrics: Optional[List[str]] = None,
        threholds: Optional[Dict[str, List[float]]] = None,
    ) -> Callable:
        """TODO:
        - Add possible options that should be appended to the log
        - Concat combination into message
        - Thresholds
        - Add index => unique id => function / method name
        - Related to ML
        - Event based calculations of inp / output => Index
        - Save to hidden directory
        - Thresholds / Quality assurance => N and Quantiles (within which range)
        - Apply sensitivity analysis? => Like add 1e4 +- to some specified
        - Focused around pandas dataframe / Pytorch Tensor / Numpy array => Standard lib in ML
        """
        log = getattr(self, "info")
        # log_warning = getattr(self, "warning")

        def wrapper(func: Callable, *args, **kwargs):
            kwargs_mapping = map_args(func, *args, **kwargs)

            if input_metrics is not None:
                if isinstance(input_metrics, dict):
                    for kw, metrics in input_metrics.items():
                        data = kwargs_mapping.get(kw, None)
                        if data is None:
                            continue

                        if not (
                            isinstance(data, pd.DataFrame)
                            or isinstance(data, np.ndarray)
                            or isinstance(data, list)
                        ):
                            raise ValueError(
                                f"{kw} must be a list, DataFrame or Numpy ndarray"
                            )
                        # Map of feat values
                        input_str = f"{func} | {kw}: "
                        input_metric_dict = dict()
                        for metric in metrics:
                            out = getattr(DataMetrics, metric)(data)
                            input_metric_dict[metric] = out
                        input_metric_dict = marshalling_dict(input_metric_dict)
                        log(input_str + input_metric_dict)

                else:
                    raise InputFormatError(
                        "The input metrics must be defined as a dictionary, where the key refers to the features"
                    )

            if _is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # TODO: Measure output

            return result

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
