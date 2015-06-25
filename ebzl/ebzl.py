import sys
import argparse

from modules import (
    create,
    bundle,
    deploy,
    env,
    help as help_,
    instances,
    list as list_
)


_MODULES = {
    "create": create,
    "bundle": bundle,
    "deploy": deploy,
    "env": env,
    "help": help_,
    "instances": instances,
    "list": list_
}


def get_module_list():
    return _MODULES.keys()


def get_module(name):
    return _MODULES.get(name)


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("action",
                        choices=get_module_list(),
                        help="Action to perform.")

    return parser


def main():
    parser = get_argument_parser()
    args = parser.parse_args(sys.argv[1:2])
    get_module(args.action).run(sys.argv[2:])


if __name__ == "__main__":
    main()
