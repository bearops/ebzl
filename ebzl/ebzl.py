import os
import sys
import argparse
import importlib


def get_module_list():
    return [os.path.splitext(m)[0] 
            for m in os.listdir("modules") 
            if m.endswith(".py") and not m.startswith("_")]


def get_module(name):
    return importlib.import_module(".%s" % name, "modules")


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
