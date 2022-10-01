"""
Definition of possible metrics to check for, including common SWE KPIs and ML KPIs
"""
import time
from typing import Any, Callable, List, Union

import numpy as np

from ._misc import _is_method

import pandas as pd
import numpy as np


class MonitorMetrics:
    @classmethod
    def execution_time(cls, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(end_time - start_time)
            return result

        return wrapper

    @classmethod
    def latency(cls):
        pass

    @classmethod
    def cpu_usage(cls):
        pass

    @classmethod
    def gpu_usage(cls):
        pass

    @classmethod
    def throughput(cls):
        pass


class DataMetrics:
    @classmethod
    def size(cls, X: Any):
        return len(X)

    @classmethod
    def nans(cls, X: Any):
        if isinstance(X, pd.DataFrame):
            return X.isna().sum().tolist()

        if isinstance(X, np.ndarray):
            return list(np.isnan(X).sum(axis=0))

        elif isinstance(X, list):
            return np.isnan(X).sum()

        else:
            raise ValueError()

    @classmethod
    def mean(cls, X: Any):
        if isinstance(X, pd.DataFrame):
            return X.mean().tolist()

        if isinstance(X, np.ndarray):
            return list(np.mean(X, axis=0))

        elif isinstance(X, list):
            return np.mean(X)

        else:
            raise ValueError()

    @classmethod
    def percentile5(cls, X):
        q = 5
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()

    @classmethod
    def percentile25(cls, X):
        q = 25
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()

    @classmethod
    def median(cls, X):
        q = 50
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()

    @classmethod
    def percentile75(cls, X):
        q = 75
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()

    @classmethod
    def percentile95(cls, X):
        q = 95
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()
