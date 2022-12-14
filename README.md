# mlog
A library with off the shelf logging of machine learning systems to remove any boilerplate code of logging I/O of pipelines. The logging class takes advantage of decorator and typestate design patterns to easily apply logging logic on I/O of functions and methods.

The library offers the option to apply thresholds to maintain a certain level of stability. In case the value exceeds the thresholds, a warning will be logged with the exact exceeding value, so it is easy to catch any shifts in the data distribution. The library has some predefined metrics such as mean, count of nans, count of duplicates, number of rows, execution time etc, but it has the option to use self-defined functions.

Currently, the library is only compatible with NumPy Arrays, Pandas DataFrames and lists. In the future, the logging will also be compatible with PyTorch Tensors.

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
