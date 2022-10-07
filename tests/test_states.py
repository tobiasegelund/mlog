import pytest

from mlog._exceptions import OutputError, InputFormatError


def test_input_df(logger, df):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func(df)


def test_input_array(logger, array):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func(array)


def test_input_list(logger):
    @logger.input.log(metrics={"i": ["mean"]})
    def test_func(i):
        pass

    test_func([10, 20, 30])


def test_output(logger):
    @logger.output.log(metrics=["mean"])
    def test_func(i=[10, 20, 30]):
        return i

    test_func()


def test_output_no_return_values(logger):
    @logger.output.log(metrics=["mean"])
    def test_func(i=[10, 20, 30]):
        pass

    with pytest.raises(OutputError) as exc_info:
        test_func()
