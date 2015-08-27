import argparse

from .. modules import (
    bundle,
    create,
    delete,
    deploy,
    ecs,
    env,
    instances,
    list as list_,
    version
)


MODULES_DICT = {
    "bundle": bundle,
    "create": create,
    "delete": delete,
    "deploy": deploy,
    "ecs": ecs,
    "env": env,
    "instances": instances,
    "list": list_,
    "version": version
}


def get_module_list():
    return MODULES_DICT.keys()


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl help")

    parser.add_argument("action",
                        help="Ebzl module.")

    return parser


def run(argv):
    args = get_argument_parser().parse_args(argv)
    try:
        MODULES_DICT.get(args.action).get_argument_parser().print_help()
    except AttributeError:
        print("Module not found: %s" % args.action)
        exit()
