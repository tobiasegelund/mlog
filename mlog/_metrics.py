"""
Definition of possible metrics to check for, including common SWE KPIs and ML KPIs
"""
from typing import Any

import numpy as np

import pandas as pd
import numpy as np


class DataMetrics:
    @classmethod
    def count(cls, X: Any):
        return len(X)

    # @classmethod
    # def mode(cls, X: Any):
    #     if isinstance(X, pd.DataFrame):
    #         return X.mode().tolist()

    #     if isinstance(X, np.ndarray):
    #         return list(np.mode(X).sum(axis=0))

    #     elif isinstance(X, list):
    #         return np.mode(X).sum()

    #     else:
    #         raise ValueError()

    @classmethod
    def duplicates(cls, X: Any):
        if isinstance(X, pd.DataFrame):
            return int(X.duplicated().sum())

        if isinstance(X, np.ndarray):
            return int(len(X) - len(np.unique(X, axis=0)))

        elif isinstance(X, list):
            return int(len(X) - len(set(X)))

        else:
            raise ValueError()

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
    def percentile1(cls, X):
        q = 1
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

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

    @classmethod
    def percentile99(cls, X):
        q = 99
        if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
            return list(np.percentile(X, q=q, axis=0))

        elif isinstance(X, list):
            return np.percentile(X, q=q)

        else:
            raise ValueError()
