from pathlib import Path
import logging
import hashlib

GIT_DIR = ".minigit"


def init():
    """
    Creates the initial .minigit folder and the objects folder.
    This function should only be called once.
    :return: None
    """
    Path(GIT_DIR).mkdir(parents=True, exist_ok=True)
    logging.debug("Created .minigit directory")
    Path(f"{GIT_DIR}/objects").mkdir(parents=True, exist_ok=True)
    logging.debug("Created .minigit/objects directory")


def hash_object(data, type_="blob"):
    """
    Hashes a given object, adds it to the minigit object store,
    and returns the hash.
    :param data: The data to hash
    :param type_: The type of object to hash
    :return: The hash of the object as a string.
    """
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha256(data).hexdigest()
    logging.debug(f"Hashed object {oid} with type {type_}")
    path = Path(".") / GIT_DIR / "objects" / oid
    path.write_bytes(obj)

    return oid


def get_object(oid, expected="blob"):
    """
    Gets an object from the object store.
    :param oid: The id of the object to get.
    :param expected: The type of object to get.
    :return: The object as bytes.
    """
    path = Path(".") / GIT_DIR / "objects" / oid
    obj = path.read_bytes()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None and type_ != expected:
        raise ValueError(f"Expected {expected}, got {type_}")

    return content
