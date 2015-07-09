from .. lib import (
    eb,
    parameters
)

import boto
import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl deploy")
    
    parameters.add_profile(parser)
    parameters.add_version_label(parser)
    parameters.add_region(parser, required=False)

    parser.add_argument("-e", "--env-name",
                        required=True,
                        help="ElasticBeanstalk environment name.")

    return parser


def deploy(args):
    kwargs = {
        "environment_name": args.env_name,
        "version_label": args.version
    }

    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        layer1.update_environment(**kwargs)
    except boto.exception.BotoServerError as exc:
        print(exc.message)


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    deploy(args)
