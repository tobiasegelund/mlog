import pytest
import pandas as pd
from mlog import Logger


@pytest.fixture
def logger():
    yield Logger()


@pytest.fixture
def df():
    data = {
        "feat1": [1, 2, 3, 4, 1],
        "feat2": [2.3, 41.0, 0.1, 2.3, 2.3],
        "feat3": [2, 3, 10, None, 2],
    }
    yield pd.DataFrame(data)


@pytest.fixture
def array(df):
    yield df.to_numpy()


@pytest.fixture
def data_list():
    yield [2, 3, 4, 8, 10]
