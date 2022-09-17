"""
Definition of possible metrics to check for, including common SWE KPIs and ML KPIs
"""
import time
from typing import Any

import numpy as np

# import pandas as pd


class MonitorMetrics:
    @classmethod
    def execution_time(cls):
        pass

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
    def mean(cls, X: Any):
        if isinstance(X, int):
            X = [X]
        return np.mean(X)

    @classmethod
    def quantile5(cls, X):
        if isinstance(X, int):
            X = [X]
        return np.quantile(X, q=0.5)

    @classmethod
    def quantile25(cls, X):
        if isinstance(X, int):
            X = [X]
        return np.quantile(X, q=0.25)

    @classmethod
    def median(cls, X):
        if isinstance(X, int):
            X = [X]
        return np.quantile(X, q=0.50)

    @classmethod
    def quantile75(cls, X):
        if isinstance(X, int):
            X = [X]
        return np.quantile(X, q=0.75)

    @classmethod
    def quantile95(cls, X):
        if isinstance(X, int):
            X = [X]
        return np.quantile(X, q=0.95)
