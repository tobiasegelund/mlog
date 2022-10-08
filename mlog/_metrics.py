"""
Definition of possible metrics to check for, including common SWE KPIs and ML KPIs
"""
from typing import Any, Callable

import numpy as np

import pandas as pd
import numpy as np

from ._exceptions import InputError


def get_data_metric(metric: str) -> Callable:
    mapping = {
        "count": count,
        "duplicates": duplicates,
        "nans": nans,
        "mean": mean,
        "percentile1": percentile1,
        "percentile5": percentile5,
        "percentile25": percentile25,
        "median": median,
        "percentile75": percentile75,
        "percentile95": percentile95,
        "percentile99": percentile99,
    }

    try:
        func = mapping.get(metric)
    except KeyError:
        raise ValueError(
            f"The metric is not available among the options. Please choose between {mapping.keys()}"
        )
    return func


def count(X: Any):
    return len(X)

    # @classmethod
    # def mode(X: Any):
    #     if isinstance(X, pd.DataFrame):
    #         return X.mode().tolist()

    #     if isinstance(X, np.ndarray):
    #         return list(np.mode(X).sum(axis=0))

    #     elif isinstance(X, list):
    #         return np.mode(X).sum()

    #     else:
    # raise InputError("{type(X)} must be a list, DataFrame or Numpy ndarray")


def duplicates(X: Any):
    if isinstance(X, pd.DataFrame):
        return int(X.duplicated().sum())

    if isinstance(X, np.ndarray):
        return int(len(X) - len(np.unique(X, axis=0)))

    elif isinstance(X, list):
        return int(len(X) - len(set(X)))

    else:
        raise ValueError()


def nans(X: Any):
    if isinstance(X, pd.DataFrame):
        return X.isna().sum().tolist()

    if isinstance(X, np.ndarray):
        return list(np.isnan(X).sum(axis=0))

    elif isinstance(X, list):
        return np.isnan(X).sum()

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def mean(X: Any):
    if isinstance(X, pd.DataFrame):
        return X.mean().tolist()

    if isinstance(X, np.ndarray):
        return list(np.mean(X, axis=0))

    elif isinstance(X, list):
        return np.mean(X)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile1(X):
    q = 1
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile5(X):
    q = 5
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile25(X):
    q = 25
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def median(X):
    q = 50
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile75(X):
    q = 75
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile95(X):
    q = 95
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")


def percentile99(X):
    q = 99
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        return list(np.percentile(X, q=q, axis=0))

    elif isinstance(X, list):
        return np.percentile(X, q=q)

    else:
        raise InputError(f"{type(X)} must be a list, DataFrame or Numpy ndarray")
