import pytest

from mlog._exceptions import OutputError, InputError


def test_input_df(logger, df):
    @logger.input.log(metrics={"i": ["mean"]})
    @logger.input.log(
        metrics={
            "i": {
                "feat1": {"mean": (1, 5)},
                "feat2": ["mean", "percentile25", "count", "nans", "duplicates"],
            }
        }
    )
    def test_func(i):
        pass

    test_func(df)


def test_input_array(logger, array):
    @logger.input.log(metrics={"i": ["mean"]})
    @logger.input.log(
        metrics={
            "i": {
                0: {"mean": (1, 5)},
                1: ["mean", "percentile25", "count", "nans", "duplicates"],
            }
        }
    )
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


def test_output_wrong_metric_input(logger):
    @logger.output.log(metrics="mean")
    def test_func(i=[10, 20, 30]):
        return i

    with pytest.raises(InputError) as exc_info:
        test_func()


def test_output_supply_self_defined_function(logger):
    def counter(X):
        return len(X)

    @logger.output.log(metrics=["mean", counter])
    def test_func(i=[10, 20, 30]):
        return i

    test_func()
