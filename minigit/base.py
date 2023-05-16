import logging
from pathlib import Path
from . import data


def write_tree(directory=Path(".")):
    entries = []
    for entry in directory.glob("*"):
        if is_ignored(entry):
            logging.debug(f"Ignored: {entry.absolute} - within .minigit folder")
            continue
        if entry.is_file() and not entry.is_symlink():
            type_ = "blob"
            logging.debug(f"File: {entry.absolute}")
            obj = entry.read_bytes()
            oid = data.hash_object(obj)
        if entry.is_dir() and not entry.is_symlink():
            type_ = "tree"
            logging.debug(f"Directory: {entry.absolute}")
            oid = write_tree(entry)

        entries.append((entry.name, oid, type_))

    tree = "".join(f"{type_} {oid} {name}\n" for name, oid, type_ in sorted(entries))

    return data.hash_object(tree.encode(), "tree")


def is_ignored(path):
    return data.GIT_DIR in path.parts
