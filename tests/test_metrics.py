import pytest
import numpy as np

from mlog._metrics import get_data_metric


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("count", 5),
        ("mean", 5.4),
        ("nans", 0),
        ("duplicates", 0),
        ("percentile1", 2.04),
        ("percentile5", 2.2),
        ("percentile25", 3.0),
        ("median", 4.0),
        ("percentile75", 8.0),
        ("percentile95", 9.6),
        ("percentile99", 9.92),
    ],
)
def test_metric_with_list(metric, expected, data_list):
    func = get_data_metric(metric)
    output = func(data_list)
    assert output == expected


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("count", 5),
        # ("mean", [2.2, 9.599999999999998, 4.25]),
        ("nans", [0, 0, 1]),
        ("duplicates", 1),
        # ("percentile1", [1.0, 0.188, np.nan]),
        # ("percentile5", [1.0, 0.5399999999999999, np.nan]),
        # ("percentile25", [1.0, 2.3, np.nan]),
        # ("median", [2.0, 2.3, np.nan]),
        # ("percentile75", [3.0, 2.3, np.nan]),
        # ("percentile95", [3.8, 33.25999999999999, np.nan]),
        # ("percentile99", [3.96, 39.452, np.nan]),
    ],
)
def test_metric_with_df(metric, expected, df):
    func = get_data_metric(metric)
    output = func(df)
    assert output == expected


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("count", 5),
        # ("mean", [2.2, 9.599999999999998, 4.25]),
        ("nans", [0, 0, 1]),
        ("duplicates", 1),
        # ("percentile1", 1),
        # ("percentile5", [1.0, 0.5399999999999999, np.nan]),
        # ("percentile25", [1.0, 2.3, np.nan]),
        # ("median", [2.0, 2.3, np.nan]),
        # ("percentile75", [3.0, 2.3, np.nan]),
        # ("percentile95", [3.8, 33.25999999999999, np.nan]),
        # ("percentile99", [3.96, 39.452, np.nan]),
    ],
)
def test_metric_with_array(metric, expected, array):
    func = get_data_metric(metric)
    output = func(array)
    assert output == expected
