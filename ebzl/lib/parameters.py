"""Input parameters commons."""

from . import (
    config,
    format as fmt
)
from ..modules import version


def add_profile(parser, required=True, honour_default=True):
    kwargs = {"required": required}

    if honour_default and config.has_default_profile():
        kwargs["default"] = config.DEFAULT_PROFILE_NAME
        kwargs["required"] = False

    parser.add_argument("-p", "--profile",
                        choices=config.get_profile_names(),
                        help="AWS credentials profile.",
                        **kwargs)


def add_app_name(parser, required=True):
    parser.add_argument("-a", "--app-name",
                        required=required,
                        help="ElasticBeanstalk application name.")


def add_version_label(parser, required=True):
    kwargs = {'required': required}
    if not required:
        kwargs['default'] = version.get_version()

    parser.add_argument("-v", "--version",
                        help="Version label.",
                        **kwargs)


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
            print(exc)
            exit()

    return args


def add_default_region(parser, args):
    if args.region:
        return

    args.region = config.get_default_region(args.profile)

    if args.region is None:
        raise Exception("Can't determine region based on AWS config file.")

    return args
