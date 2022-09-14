from functools import wraps

from ._metrics import latency
from ._misc import _is_method


def profiling():
    def wrapper(func):
        if isinstance(func, callable):
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

