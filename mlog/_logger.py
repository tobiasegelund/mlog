import logging
from typing import Callable, Literal, Optional, Dict, List
from functools import wraps, partial

from ._misc import _is_method, extract_args_dict
from ._exceptions import ArgumentNotCallable, ModeError
from ._metrics import DataMetrics
from ._format import marshalling_dict


class Logger:
    """High-level inferface of the logger class

    A class to handle logging of deployed machine learnings models, including tracing and profiling.

    Params:


    Usage:
        >>>
        >>>

    """

    def __init__(
        self,
        format: str = "%(asctime)s | %(levelname)s | %(message)s",
        level=logging.INFO,
    ) -> None:
        # TODO: Update type param for level
        logging.basicConfig(format=format, level=level)
        self.logger = logging.getLogger(__name__)

    # TODO: Divide the log by level into multiple logs if wanted
    # def add(self, key: str) -> None:
    #     # Add more output files
    #     # val = getattr(self, key)
    #     pass

    def log(
        self,
        func: Optional[Callable] = None,
        *,
        message: str = "",
        input_metrics: Optional[Dict[str, List[str]]] = None,
        output_metrics: Optional[List[str]] = None,
        mode: Literal["info", "warning", "error"] = "info",
    ) -> Callable:
        """TODO:
        - Add possible options that should be appended to the log
        - Concat combination into message
        - Add index => unique id
        - Related to ML
        - Event based calculations of input / output
        - Save to hidden directory
        - Focused around pandas dataframe / Pytorch / Numpy array => Standard lib in ML
        """
        if mode not in ("info", "warning", "error"):
            raise ModeError(
                f"{mode} is not a possible mode. Please choose among ['info', 'warning', 'error']"
            )
        log = getattr(self, mode)
        if len(message) > 0:
            log(message)

        def wrapper(func: Callable, *args, **kwargs):
            args_mapping = extract_args_dict(func, *args, **kwargs)
            print(args_mapping)

            if input_metrics is not None:
                for key, metrics in input_metrics.items():
                    input = args_mapping.get(key, None)
                    if input is None:
                        self.warning(f"{key} is not an optional argument")
                        continue

                    output_metrics = f"{key}: "
                    d = dict()
                    for metric in metrics:
                        out = getattr(DataMetrics, metric)(input)
                        d[metric] = round(out, 2)
                        # output_metrics += f"{metric}={out: .1f}, "
                    d = marshalling_dict(d)
                    log(output_metrics + d)

            # input = self._concat_msg(*args, **kwargs)
            # if len(input) > 0:
            #     log(input)
            # log(mean)

            if _is_method(func):
                return func(self, *args, **kwargs)
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

    def _concat_msg(self, *args, **kwargs) -> str:
        msg = ""
        if len(args) > 0:
            msg += "args=" + str(args)
        if len(kwargs) > 0:
            msg += "| kwargs=" + str(kwargs)

        return msg

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)
