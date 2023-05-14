import os
import logging
import hashlib

GIT_DIR = ".minigit"


def init():
    os.mkdir(GIT_DIR)
    logging.debug("Created .minigit directory")


def hash_object(data):
    oid = hashlib.sha256(data).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(data)
    return oid
