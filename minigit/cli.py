import argparse
import logging
import os
from . import data
from . import base


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    logging.info("parse args")
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file", type=str)

    cat_file_parser = commands.add_parser("cat-file")
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object")

    return parser.parse_args()


def init(args):
    data.init()
    logging.debug(f"Initialized data directory in {os.getcwd()}/{data.GIT_DIR}")


def hash_object(args):
    with open(args.file, "rb") as f:
        logging.debug(f"Hashing {args.file}: {data.hash_object(f.read())}")


def cat_file(args):
    logging.debug(f"Cat file: {args.object} Hash: {data.get_object(args.object, expected=None)}")
