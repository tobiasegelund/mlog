from typing import Callable, Optional
from functools import wraps

from ._metrics import latency
from ._misc import _is_method


def profiling(
    func: Optional[Callable] = None,
    *,
    execution_time: bool = True,
    cpu_usage: bool = True,
    gpu_usage: bool = True,
    throughput: bool = False,
):
    def wrapper(func):
        if callable(func):
            if _is_method(func):

                @wraps(func)
                def inner(self, *args, **kwargs):
                    func(self)

                return inner
            else:

                @wraps(func)
                def inner(*args, **kwargs):
                    func()

                return inner

    return wrapper
