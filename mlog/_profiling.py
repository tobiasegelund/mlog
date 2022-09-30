from typing import Callable, Optional
from functools import wraps, partial

from ._metrics import MonitorMetrics
from ._misc import _is_method
from ._exceptions import ArgumentNotCallable


def profiling(
    func: Optional[Callable] = None,
    *,
    execution_time: bool = True,
    cpu_usage: bool = True,
    gpu_usage: bool = True,
    throughput: bool = False,
):
    def wrapper(func: Callable, *args, **kwargs):
        if execution_time:
        # if _is_method(func):
        #     return func(self, *args, **kwargs)
        return func(*args, **kwargs)

    if func is not None:
        if not callable(func):
            raise ArgumentNotCallable(
                "Not a callable. Did you use a non-keyword argument?"
            )
        return wraps(func)(partial(wrapper, func))

    def wrap_callable(func: Callable) -> Callable:
        return wraps(func)(partial(wrapper, func))

    return wrap_callable
