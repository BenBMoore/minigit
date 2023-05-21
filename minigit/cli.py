import argparse
import logging
from pathlib import Path
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

    write_tree_parser = commands.add_parser("write-tree")
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser("read-tree")
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument("tree")

    return parser.parse_args()


def init(args):
    data.init()
    logging.debug(f"Initialized data directory in {Path().absolute()}/{data.GIT_DIR}")


def hash_object(args):
    path = Path(".") / args.file
    obj = path.read_bytes()
    logging.debug(f"Hashing {path.name}: {data.hash_object(obj)}")


def cat_file(args):
    logging.debug(
        f"Cat file: {args.object} Hash: {data.get_object(args.object, expected=None)}"
    )


def write_tree(args):
    logging.debug(f"Write tree: {base.write_tree()}")


def read_tree(args):
    logging.debug(f"Read tree: {base.read_tree(args.tree)}")
