import sys
import argparse

from modules import (
    create,
    deploy,
    env,
    help as help_,
    instances,
    list as list_
)


def get_module_list():
    return [
        "create",
        "deploy",
        "env",
        "help",
        "instances",
        "list"
    ]


def get_module(name):
    d = {
        "create": create,
        "deploy": deploy,
        "env": env,
        "help": help_,
        "instances": instances,
        "list": list_
    }

    return d.get(name)


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
