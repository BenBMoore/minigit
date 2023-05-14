import os
import logging

GIT_DIR = ".minigit"


def init():
    os.mkdir(GIT_DIR)
    logging.debug("Created .minigit directory")
