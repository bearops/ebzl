#!/usr/bin/env python
from . import (
    config,
    format as fmt
)


APP_ARGS = ("-a", "--app-name")

APP_KWARGS = {
    "required": False,
    "help": "ElaticBeanstalk application name."
}


def add_profile(parser, required=True):
    parser.add_argument("-p", "--profile",
                        required=required,
                        choices=config.get_profile_names(),
                        help="AWS credentials profile.")


def add_app_name(parser, required=True):
    kwargs = APP_KWARGS
    kwargs["required"] = required

    parser.add_argument(*APP_ARGS, **kwargs)


def add_version_label(parser, required=True):
    parser.add_argument("-v", "--version",
                        required=required,
                        help="Version label.")


def add_region(parser, required=True):
    parser.add_argument("-r", "--region",
                        required=required,
                        help=("AWS region (only needed if the S3 buckets "
                              "needs to be created)."))


def add_force(parser):
    parser.add_argument("-F", "--force",
                        action="store_true",
                        help="Force, overwrite & burn things in the process.")


def add_format(parser, default=fmt.TEXT, choices=fmt.CHOICES):
    parser.add_argument("f", "--format",
                        default=default,
                        choices=choices,
                        help="Output format.")


def parse(parser, argv, postprocessors=None):
    postprocessors = postprocessors or []

    args = parser.parse_args(argv)

    for postprocessor in postprocessors:
        try:
            postprocessor(parser=parser, args=args)
        except Exception as exc:
            parser.print_usage()
            print exc
            exit()

    return args


def add_default_region(parser, args):
    if args.region:
        return

    args.region = config.get_default_region(args.profile)

    if args.region is None:
        raise Exception("Can't determine region based on AWS config file.")

    return args
