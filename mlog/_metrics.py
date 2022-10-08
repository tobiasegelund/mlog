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


# def mode(X: Any):
#     if isinstance(X, pd.DataFrame):
#         return X.mode().tolist()

#     if isinstance(X, np.ndarray):
#         return list(np.mode(X).sum(axis=0))

#     elif isinstance(X, list) or isinstance(X, pd.Series):
#         return np.mode(X).sum()

#     else:
# raise InputError("{X} must be a list, DataFrame or Numpy ndarray")


def duplicates(X: Any):
    if isinstance(X, pd.DataFrame):
        return int(X.duplicated().sum())
    try:
        if isinstance(X, np.ndarray) and len(X.shape) > 1:
            return int(len(X) - len(np.unique(X, axis=0)))
    except AttributeError:
        return int(len(X) - len(set(X)))

    return int(len(X) - len(set(X)))


def nans(X: Any):
    if isinstance(X, pd.DataFrame):
        return X.isna().sum().tolist()
    try:
        if isinstance(X, np.ndarray) and len(X.shape) > 1:
            return list(np.isnan(X).sum(axis=0))
    except AttributeError:
        return np.isnan(X).sum()

    return np.isnan(X).sum()


def mean(X: Any):
    if isinstance(X, pd.DataFrame):
        return X.mean().tolist()
    try:
        if isinstance(X, np.ndarray) and len(X.shape) > 1:
            return list(np.mean(X, axis=0))

    except AttributeError:
        return np.mean(X)
    return np.mean(X)


def percentile1(X):
    q = 1
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def percentile5(X):
    q = 5
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def percentile25(X):
    q = 25
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def median(X):
    q = 50
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def percentile75(X):
    q = 75
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def percentile95(X):
    q = 95
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)


def percentile99(X):
    q = 99
    try:
        if (isinstance(X, np.ndarray) and len(X.shape) > 1) or isinstance(
            X, pd.DataFrame
        ):
            return list(np.percentile(X, q=q, axis=0))
    except AttributeError:
        return np.percentile(X, q=q)

    return np.percentile(X, q=q)
