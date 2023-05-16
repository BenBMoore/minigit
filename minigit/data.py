from pathlib import Path
import logging
import hashlib

GIT_DIR = ".minigit"


def init():
    Path(GIT_DIR).mkdir(parents=True, exist_ok=True)
    logging.debug("Created .minigit directory")
    Path(f"{GIT_DIR}/objects").mkdir(parents=True, exist_ok=True)
    logging.debug("Created .minigit/objects directory")


def hash_object(data, type_="blob"):
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha256(data).hexdigest()
    path = Path(".") / GIT_DIR / "objects" / oid
    path.write_bytes(obj)
    return oid


def get_object(oid, expected="blob"):
    path = Path(".") / GIT_DIR / "objects" / oid
    obj = path.read_bytes()

    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()

    if expected is not None and type_ != expected:
        raise ValueError(f"Expected {expected}, got {type_}")

    return content
