import argparse
import logging
import os
from . import data


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=data.hash_object)
    hash_object_parser.add_argument("path", type=str)

    return parser.parse_args()


def init(args):
    data.init()
    logging.debug(f"Initialized data directory in {os.getcwd()}/{data.GIT_DIR}")


def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))
