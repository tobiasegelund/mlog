import os
import inspect
from typing import Callable
from pathlib import Path


def create_dir_if_not_exists(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def find_root_dir() -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__)))


def find_hidden_mlog_dir() -> Path:
    root_dir = find_root_dir()
    return root_dir.joinpath(".mlog")


def find_path_of_callable(func: Callable) -> str:
    return inspect.getfile(func)
