import pytest
from mlog._format import marshalling_dict, marshalling_kwargs, validate_dtype
from mlog._exceptions import DataTypeError


def test_marshalling_kwargs():
    mapping = marshalling_kwargs(a=2, b=3)
    assert mapping == '{"a": 2, "b": 3}'


def test_marshalling_dict():
    d = {
        "a": 2,
        "b": 3,
    }
    mapping = marshalling_dict(d)
    assert mapping == '{"a": 2, "b": 3}'


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
