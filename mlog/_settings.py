from ._os import create_dir_if_not_exists

HIDDEN_DIR = ".mlog"


def _settings():
    create_dir_if_not_exists(HIDDEN_DIR)
