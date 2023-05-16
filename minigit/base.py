import logging
from pathlib import Path
from . import data


def write_tree(directory="."):
    path = Path(directory)
    for entry in path.rglob("*"):
        if entry.is_dir() and not entry.is_symlink():
            logging.debug(f"Directory: {entry.absolute}")
            ## Are we handling directories or just writing files to the object store?
        if entry.is_file() and not entry.is_symlink():
            logging.debug(f"File: {entry.absolute}")
            # Write file
