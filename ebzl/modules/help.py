import argparse

from .. modules import (
    create,
    deploy,
    env,
    instances,
    list as list_
)


def get_module_list():
    return [
        "create",
        "deploy",
        "env",
        "instances",
        "list"
    ]


def get_module(name):
    d = {
        "create": create,
        "deploy": deploy,
        "env": env,
        "instances": instances,
        "list": list_
    }

    return d.get(name)


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("action",
                        help="Ebzl module.")

    return parser


def run(argv):
    args = get_argument_parser().parse_args(argv)
    get_module(args.action).get_argument_parser().print_help()
