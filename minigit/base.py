import logging
from pathlib import Path
from . import data


def write_tree(directory=Path(".")):
    """
    Write a tree object from a directory.

    Args:
        directory (Path): The directory to write the tree object from.

    Returns:
        str: The tree object's SHA-1 hash.
    """
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


def _iter_tree_entries(oid):
    """
    Iterate over the entries in a tree object.

    Args:
        oid (str): The tree object's SHA-256 hash.
    """
    if not oid:
        return
    tree = data.get_object(oid, "tree")
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(" ", 2)
        yield type_, oid, name


def get_tree(oid, base_path=Path(".")):
    """
    Gets the tree structure from a given path

    Args:
        oid (str): The tree object's SHA-1 hash.
        base_path (Path): The base path to start from.

    Returns:
        dict: A dictionary of the tree structure.
        {
            Path("path/to/file"): "oid",
            Path("path/to/directory"): "oid"
        }
    """
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        if type_ == "blob":
            path = base_path / name
            result[path] = oid
        elif type_ == "tree":
            path = base_path / name
            result.update(get_tree(oid, base_path=path))
        else:
            raise ValueError(f"Invalid type: {type_}")

    return result


def read_tree(tree_oid):
    """
    Read a tree object, and write to the working directory

    Args:
        tree_oid (str): The tree object's SHA-1 hash.
    """

    for path, oid in get_tree(tree_oid, Path(".")).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.get_object(oid))


def is_ignored(path):
    """
    Check if a path is ignored.

    Args:
        path (Path): The path to check.

    Returns:
        bool: True if the path is ignored, False otherwise.
    """

    return data.GIT_DIR in path.parts
