import argparse
import importlib


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("action", 
                        help="Ebzl module.")

    return parser


def get_module_list():
    return [os.path.splitext(m)[0] 
            for m in os.listdir("modules") 
            if m.endswith(".py") and not m.startswith("_")]


def get_module(name):
    return importlib.import_module(".%s" % name, "modules")


def run(argv):
    args = get_argument_parser().parse_args(argv)
    get_module(args.action).get_argument_parser().print_help()

