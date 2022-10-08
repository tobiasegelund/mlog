import pytest
from mlog._utils import map_args, is_method, validate_dtype
from mlog._exceptions import DataTypeError


def test_map_args():
    def wrap(a, b, c, d):
        pass

    mapping = map_args(wrap, 2, 3, 4, d=2)

    assert list(mapping.keys()) == ["a", "b", "c", "d"]
    assert list(mapping.values()) == [2, 3, 4, 2]


def test_is_method():
    def function():
        pass

    class Test:
        def method(self):
            pass

    assert is_method(Test.method) == True
    assert is_method(function) == False


@pytest.mark.parametrize(
    "input, dtype", [([10, 20, 30], int), ([10, 20, 30], [int, float])]
)
def test_validate_dtype(input, dtype):
    validate_dtype(input=input, expected_dtype=dtype)


@pytest.mark.parametrize(
    "input, dtype", [([10, 20, 30], str), ([10, 20, 30, "as"], [int, float])]
)
def test_validate_dtype_error(input, dtype):
    with pytest.raises(DataTypeError) as exc_info:
        validate_dtype(input=input, expected_dtype=dtype)
