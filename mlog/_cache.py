"""
Functions used to create and clear cache in the hidden directory .mlog

Collect and analyze etc.
"""
import json
from pathlib import Path

from ._os import find_hidden_mlog_dir


def clear_cache() -> None:
    pass


def update_cache(data: str, path: Path) -> None:
    with open(path, "w") as f:
        f.write(data)


def load_cache(self) -> None:
    path = find_hidden_mlog_dir()

    maps = []
    for file in ["profile.tmp", "input.tmp", "output.tmp"]:
        if (path := path.joinpath(file)).exists():
            with open(path, "r") as f:
                maps.append(json.load(f))
        else:
            maps.append({})  # Empty dict to uses

    self.mappings = dict(zip(["profile", "input", "output"], maps))
