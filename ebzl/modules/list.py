from .. lib import (
    eb,
    parameters
)

import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl list")

    parameters.add_profile(parser)
    parameters.add_app_name(parser)
    parameters.add_region(parser, required=False)

    return parser


def list_versions(args):
    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_application_versions(application_name=args.app_name)

    versions = (data["DescribeApplicationVersionsResponse"]
                    ["DescribeApplicationVersionsResult"]
                    ["ApplicationVersions"])

    for version in versions:
        print version["VersionLabel"]


def list_applications(args):
    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_applications()

    apps = (data['DescribeApplicationsResponse']
                ['DescribeApplicationsResult']
                ['Applications'])

    for app in apps:
        print app["ApplicationName"]


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.app_name:
        list_versions(args)
    else:
        list_applications(args)
