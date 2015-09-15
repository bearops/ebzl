import os
import argparse

from .. lib import (
    eb,
    s3,
    parameters
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl delete")

    parameters.add_profile(parser)
    parameters.add_app_name(parser)
    parameters.add_version_label(parser, required=True)
    parameters.add_region(parser, required=False)

    return parser


def delete_eb_version(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    kwargs = {
        "application_name": args.app_name,
        "version_label": args.version,
        "delete_source_bundle": False
    }

    try:
        layer1.delete_application_version(**kwargs)
    except boto.exception.BotoServerError as exc:
        print(exc.message)
        exit()


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    delete_eb_version(args)
