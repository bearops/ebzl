import argparse

from .. modules import (
    bundle,
    create,
    deploy,
    env,
    instances,
    list as list_,
    version
)


def get_module_list():
    return [
        "bundle",
        "create",
        "deploy",
        "env",
        "instances",
        "list",
        "version"
    ]


def get_module(name):
    d = {
        "bundle": bundle,
        "create": create,
        "deploy": deploy,
        "env": env,
        "instances": instances,
        "list": list_,
        "version": version
    }

    return d.get(name)


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl help")

    parser.add_argument("action",
                        help="Ebzl module.")

    return parser


def run(argv):
    args = get_argument_parser().parse_args(argv)
    try:
        get_module(args.action).get_argument_parser().print_help()
    except AttributeError:
        print("Module not found: %s" % args.action)
        exit()
