import sys
import datetime
from abc import abstractmethod, ABC
from typing import Callable, Optional, Dict, List, Union, Tuple
from functools import wraps, partial

import pandas as pd
import numpy as np

from ._misc import is_method, map_args
from ._exceptions import ArgumentNotCallable, InputFormatError
from ._metrics import DataMetrics
from ._format import marshalling_dict, convert_bytes_to_gb, convert_bytes_to_mb


class LogState(ABC):
    @abstractmethod
    def log(self) -> Callable:
        pass


class LogProfile:
    def __init__(self, _parent) -> None:
        self._parent = _parent

    def log(
        self,
        func: Optional[Callable] = None,
        *,
        execution_time: bool = False,  # Specify format?
        cpu_usage: bool = False,
        gpu_usage: bool = False,
        memory_usage: bool = False,
    ) -> Callable:
        """TODO:
        - Add possible options that should be appended to the log
        - Thresholds
        - Add index => unique id => function / method name
        - Event based calculations of inp / output => Index
        - Save to hidden directory
        - Thresholds / Quality assurance => N and Quantiles (within which range)
        - Apply sensitivity analysis? => Like add 1e4 +- to some specified
        - Focused around pandas dataframe / Pytorch Tensor / Numpy array => Standard lib in ML
        - Change all future exceptions with warnings instead
        """
        start_time = datetime.datetime.now()
        log = getattr(self._parent, "info")
        # log_warning = getattr(self._parent, "warning")
        # log_error = getattr(self._parent, "error")

        def wrapper(func: Callable, *args, **kwargs):
            kwargs_mapping = map_args(func, *args, **kwargs)
            profiling_dict = {}

            log_str = f"{func.__qualname__} | PROFILING | "
            if memory_usage is True:
                total = 0
                for kw, data in kwargs_mapping.items():
                    total += sys.getsizeof(data)

                profiling_dict["memory_usage"] = convert_bytes_to_mb(total)

            if is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if execution_time is True:
                end_time = datetime.datetime.now()
                profiling_dict["execution_time"] = str(end_time - start_time)  # seconds

            # profiling_dict = marshalling_dict(profiling_dict)
            log(log_str + str(profiling_dict))

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


class LogInput:
    """
    TODO:
    Data quality:
        - Validate data types
        - Checking schemas (Correct naming, correct order) => Insert prefined schema (e.g. dataframe feature names)
        - Syntax errors

        - Add mode, standard deviation, variance, frequency
        - Aggregates as sum, count, and
    """

    def __init__(self, _parent) -> None:
        self._parent = _parent

    def log(
        self,
        func: Optional[Callable] = None,
        *,
        metrics: Optional[Dict[str, List[Union[str, Callable]]]] = None,
        threholds: Optional[Dict[str, List[float]]] = None,
    ) -> Callable:
        log = getattr(self._parent, "info")
        # log_warning = getattr(self._parent, "warning")
        # log_error = getattr(self._parent, "error")

        def wrapper(func: Callable, *args, **kwargs):
            kwargs_mapping = map_args(func, *args, **kwargs)

            if metrics is not None:
                if isinstance(metrics, dict):
                    log_str = f"{func.__qualname__} | INPUT | "
                    for kw, _metrics in metrics.items():
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
                        # TODO: Map of feat values
                        log_str += f"{kw}: "
                        input_metric_dict = dict()
                        for metric in _metrics:
                            if callable(metric):
                                try:
                                    out = metric(data)
                                except Exception as e:  # TODO: Better exception handling
                                    raise ValueError("Function failed due to {e}")
                            else:
                                try:
                                    out = getattr(DataMetrics, metric)(data)
                                except AttributeError:
                                    raise ValueError(
                                        f"{metric} is not a possible metric"
                                    )
                            input_metric_dict[metric] = out
                        # TODO: Save input metric dict
                        # input_metric_dict = marshalling_dict(input_metric_dict)
                        log_str += str(input_metric_dict)
                        log(log_str)

                else:
                    raise InputFormatError(
                        "The input metrics must be defined as a dictionary, where the key refers to the features"
                    )

            if is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

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


class LogOutput:
    def __init__(self, _parent) -> None:
        self._parent = _parent

    def log(
        self,
        func: Optional[Callable] = None,
        *,
        metrics: Optional[List[Union[str, Callable]]] = None,
        threholds: Optional[Dict[str, Union[Tuple[float], List[float]]]] = None,
    ) -> Callable:
        """
        Apply certain thresholds to meet downstream criterias
        Load and analyze the input here => Any data shifts or outliers?
        """

        log = getattr(self._parent, "info")
        # log_warning = getattr(self._parent, "warning")
        # log_error = getattr(self._parent, "error")

        def wrapper(func: Callable, *args, **kwargs):
            log_str = f"{func.__qualname__} | OUTPUT |"
            output_dict = {}

            if is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)
            if metrics is not None:
                for metric in metrics:
                    if callable(metric):
                        out = metric(result)
                    else:
                        try:
                            out = getattr(DataMetrics, metric)(result)
                        except AttributeError:
                            raise ValueError(
                                f"{metric} is not available among the options"
                            )

                    output_dict[metric] = out

                log(log_str + str(output_dict))

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
