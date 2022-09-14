import pytest
from mlog import Logger


@pytest.fixture
def logger():
    yield Logger("")
