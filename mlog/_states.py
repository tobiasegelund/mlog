"""
TODO:
    - Focused around pandas dataframe / Pytorch Tensor / Numpy array => Standard lib in ML
    - Add UUID / Run id to match failures etc if it runs concurrently
    - Add index => unique id => function / method name

    - Validate data types
    - Checking schemas (Correct naming, correct order) => Insert prefined schema (e.g. dataframe feature names)
    - Syntax errors

    - Add mode, standard deviation, variance, frequency
    - Aggregates as sum, count, and
"""

import sys
import datetime
from abc import abstractmethod, ABC
from typing import Callable, Optional, Dict, List, Union, Tuple, Any
from functools import wraps, partial

import pandas as pd
import numpy as np

from ._utils import is_method, map_args, hash_string, validate_dtype
from ._exceptions import (
    ArgumentNotCallable,
    InputError,
    OutputError,
    MetricFunctionError,
)
from ._metrics import get_data_metric
from ._format import convert_bytes_to_gb, convert_bytes_to_mb


class LogState(ABC):
    def __init__(self, _parent) -> None:
        self._parent = _parent

        self.log_info = getattr(_parent, "info")
        self.log_warning = getattr(_parent, "warning")
        self.log_error = getattr(_parent, "error")

    def _calculate_metric(self, data: Any, metric: Union[Callable, str]) -> float:
        if callable(metric):
            out = metric(data)
        else:
            try:
                out = get_data_metric(metric)(data)
            except AttributeError:
                raise MetricFunctionError(
                    f"{metric} is not an available option among the standard metrics. You can add the callable function itself to the metrics."
                )

        return out

    def _calculate_metrics(
        self, data: Any, metrics: List[Union[str, Callable]]
    ) -> Dict[str, Any]:
        validate_dtype(input=metrics, expected_dtype=[str, Callable])

        metric_dict = dict()
        for metric in metrics:
            out = self._calculate_metric(data=data, metric=metric)

            try:
                metric_dict[metric.__name__] = out
            except AttributeError:
                metric_dict[metric] = out

        return metric_dict

    @abstractmethod
    def log(self) -> Callable:
        pass


class LogProfile(LogState):
    def log(
        self,
        func: Optional[Callable] = None,
        *,
        execution_time: bool = False,  # Specify format?
        memory_usage: bool = False,
        run_id: Optional[str] = None,
    ) -> Callable:
        start_time = datetime.datetime.now()

        def wrapper(func: Callable, *args, **kwargs):
            kwargs_mapping = map_args(func, *args, **kwargs)
            profiling_dict = {}

            log_str = f"{func.__qualname__} | PROFILING | "
            if memory_usage is True:
                total = 0
                for data in kwargs_mapping.values():
                    total += sys.getsizeof(data)

                profiling_dict["memory_usage"] = convert_bytes_to_mb(total)

            if is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if execution_time is True:
                end_time = datetime.datetime.now()
                profiling_dict["execution_time"] = str(end_time - start_time)  # seconds

            self.log_info(log_str + str(profiling_dict))

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


class LogInput(LogState):
    def log(
        self,
        func: Optional[Callable] = None,
        *,
        metrics: Optional[Dict[str, Union[Dict, List[Union[str, Callable]]]]] = None,
        run_id: Optional[str] = None,
    ) -> Callable:
        """

        Usages:
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
        """
        run_id = hash_string(str(datetime.datetime.now()), length=6)

        def wrapper(func: Callable, *args, **kwargs):
            kwargs_mapping = map_args(func, *args, **kwargs)
            log_str = f"{func.__qualname__} | INPUT | "

            if metrics is not None:
                if not isinstance(metrics, dict):
                    raise InputError(
                        f"The argument metrics is a {type(metrics)} object. Only dictionary is allowed."
                    )

                kw_dict = {}
                for kw, inner_metrics in metrics.items():
                    data = kwargs_mapping.get(kw, None)
                    if data is None:
                        continue

                    if isinstance(inner_metrics, list):
                        metric_dict = self._calculate_metrics(
                            data=data, metrics=inner_metrics
                        )

                        kw_dict[kw] = metric_dict

                    elif isinstance(inner_metrics, dict):
                        for feature, rules_or_metrics in inner_metrics.items():
                            feature_dict = {}
                            if isinstance(feature, str) and isinstance(
                                data, pd.DataFrame
                            ):
                                try:
                                    feat_data = data[feature]
                                except KeyError:
                                    self.log_warning(
                                        f"{feature} not available a feature in {kw}"
                                    )
                                    continue

                            elif isinstance(feature, int) and isinstance(
                                data, pd.DataFrame
                            ):
                                try:
                                    feat_data = data.iloc[:, feature]
                                except KeyError:
                                    self.log_warning(
                                        f"{feature} not available a feature in {kw}"
                                    )
                                    continue

                            elif isinstance(feature, int) and isinstance(
                                data, np.ndarray
                            ):
                                try:
                                    feat_data = data[:, feature]
                                except IndexError:
                                    self.log_warning(
                                        f"Index {feature} is out of range in {kw}"
                                    )
                                    continue
                            else:
                                raise InputError(
                                    f"The combination of {type(feature)} and {type(data)} is currently not possible to filter on"
                                )

                            if isinstance(rules_or_metrics, dict):
                                metric_dict = {}
                                for metric, params in rules_or_metrics.items():
                                    if params is not None:
                                        validate_dtype(
                                            input=params,
                                            expected_dtype=[int, float],
                                        )
                                        out = self._calculate_metric(
                                            data=feat_data, metric=metric
                                        )
                                        lower_bound, upper_bound = params
                                        if out < lower_bound or out > upper_bound:
                                            self.log_warning(
                                                f"{func.__qualname__} | {kw} - {feature} | {metric}: {out} out of bounds [{lower_bound}, {upper_bound}]"
                                            )

                                    else:
                                        out = self._calculate_metric(
                                            data=feat_data, metric=metric
                                        )

                                    try:
                                        metric_dict[metric.__name__] = out
                                    except AttributeError:
                                        metric_dict[metric] = out

                            elif isinstance(rules_or_metrics, list):
                                metric_dict = self._calculate_metrics(
                                    data=feat_data,
                                    metrics=rules_or_metrics,  # TODO: Better variable name
                                )

                            else:
                                raise InputError(
                                    f"The argument metrics holds a {type(rules_or_metrics)} object. Only dictionary and lists are allowed."
                                )
                            feature_dict[feature] = metric_dict
                            kw_dict[kw] = feature_dict

                    else:
                        raise InputError(
                            f"The argument metrics is a {type(metrics)} object. Only dictionary is allowed."
                        )

                self.log_info(log_str + str(kw_dict))

            if is_method(func):
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


class LogOutput(LogState):
    def log(
        self,
        func: Optional[Callable] = None,
        *,
        metrics: Optional[
            Union[
                Dict[
                    Union[str, Callable],
                    Optional[Tuple[float, float]],
                ],
                List[Union[str, Callable]],
            ]
        ] = None,
        run_id: Optional[str] = None,
    ) -> Callable:
        """

        Usage:
            >>> logger.output.log(metrics={"mean": (0.5, 0.8), "percentile10": None})
            >>> def func(X):
            >>>     return X

            >>> logger.output.log(metrics=["mean", "percentile1"])
            >>> def func(X):
            >>>     return X
        """
        run_id = hash_string(
            str(datetime.datetime.now()), length=6
        )  # TODO: Make run id across input, output and profile

        def wrapper(func: Callable, *args, **kwargs):
            log_str = f"{func.__qualname__} | OUTPUT | "
            output_dict = {}

            if is_method(func):
                result = func(self, *args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if result is None:
                self.log_error(
                    f"{func.__qualname__} does not return any values. Impossible to run any statistics on the output."
                )
                return result

            if metrics is not None:
                if isinstance(metrics, dict):
                    for metric, params in metrics.items():
                        if params is not None:
                            # TODO: Validate dtypes to floats/ints
                            if (l := len(params)) != 2:
                                raise ValueError(
                                    f"{l} parameters supplied to {metric}. Please use following format: '{metric}': (x_l, x_u) or '{metric}': None"
                                )
                            validate_dtype(params, expected_dtype=[float, int])

                            out = self._calculate_metric(data=result, metric=metric)
                            lower_bound, upper_bound = params
                            if out < lower_bound or out > upper_bound:
                                self.log_warning(
                                    f"{func.__qualname__} | {metric}: {out} out of bounds [{lower_bound}, {upper_bound}]"
                                )
                        else:
                            out = self._calculate_metric(data=result, metric=metric)

                        try:
                            output_dict[metric.__name__] = out
                        except AttributeError:
                            output_dict[metric] = out

                elif isinstance(metrics, list):
                    output_dict = self._calculate_metrics(data=result, metrics=metrics)

                else:
                    raise InputError(
                        f"The argument metrics is a {type(metrics)} object. Only dictionary and lists are allowed."
                    )

                self.log_info(log_str + str(output_dict))

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
