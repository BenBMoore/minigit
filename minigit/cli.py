import argparse
import logging
import os
from . import data


def main ():
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args ()
    args.func (args)


def parse_args ():
    parser = argparse.ArgumentParser ()

    commands = parser.add_subparsers (dest='command')
    commands.required = True

    init_parser = commands.add_parser ('init')
    init_parser.set_defaults (func=init)

    return parser.parse_args ()


def init (args):
    data.init()
    logging.debug(f'Initialized data directory in {os.getcwd()}/{data.GIT_DIR}')