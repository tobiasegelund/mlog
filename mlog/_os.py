import os


def create_dir_if_not_exists(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)
