#!/usr/bin/env python
from . import config


def add_profile(parser):
    parser.add_argument("-p", "--profile",
                        required=True,
                        choices=config.get_profile_names(),
                        help="AWS credentials profile.")


def add_app_name(parser):
    parser.add_argument("-a", "--app-name",
                        required=True,
                        help="ElasticBeanstalk application name.")


def add_version_label(parser):
    parser.add_argument("-v", "--version",
                        required=True,
                        help="Version label.")


def add_region(parser, required=True):
    parser.add_argument("-r", "--region",
                        required=required,
                        help=("AWS region (only needed if the S3 buckets "
                              "needs to be created)."))


def add_force(parser):
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Force, overwrite & burn things in the process.")


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
