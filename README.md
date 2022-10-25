# mlog
A library with off the shelf logging and monitoring of machine learning systems. The logging class takes advantage of decorator and typestate design patterns to easily apply logging logic on input and output of functions and methods.

Its focus is on batch predictions of machine learning systems. It logs and monitors any changes in input and output data of functions to catch data shifts as soon as possible, and remove boilerplate logging code in order to achieve level of logging of machine learning pipelines. The library has some predefined metrics such as mean, nans, number of duplicated, number of rows, execution time etc, including self-defined functions is easy to apply.

The library offers the option to set thresholds to maintain a certain level of stability in the I/O of machine learning systems. In case the value is not within the threshold, a warning will be logged with the exact metric and thresholds.

Currently, the library is only compatible with NumPy arrays, Pandas DataFrames or lists. In the future, the logging will also be compatible with PyTorch Tensors.

## Installation
To install the latest version of the library use the following command

```bash
pip install git+https://github.com/tobiasegelund/mlog.git
```

or

```bash
pip install git+https://github.com/tobiasegelund/mlog.git@0.1.0
```

## Usage
```python
from mlog import Logger
import pandas as pd

logger = Logger()

@logger.profile.log(execution_time=True, memory_usage=True)
@logger.input.log(metrics={"df": {"feat1": ["mean", "size"]}})
@logger.output.log(metrics=["mean", "size"])
def test(df: pd.DataFrame) -> pd.Series:
    # processing df to x
    return x


@logger.profile.log(execution_time=True, memory_usage=True)
@logger.input.log(metrics={"df": {"feat1": {"mean": (5, 8)}}})
@logger.output.log(metrics={"mean": (2, 10)})
def test(df: pd.DataFrame) -> pd.Series:
    # processing df to x
    return x


# Standard logging can also be used
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```
