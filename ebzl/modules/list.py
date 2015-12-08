from .. lib import (
    eb,
    parameters
)

import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl list")

    parameters.add_profile(parser, required=False)
    parameters.add_app_name(parser, required=False)
    parameters.add_region(parser, required=False)

    parser.add_argument("-E", "--list-envs",
                        action="store_true",
                        help="List application's environments.")

    return parser


def list_versions(args):
    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_application_versions(application_name=args.app_name)

    versions = (data["DescribeApplicationVersionsResponse"]
                    ["DescribeApplicationVersionsResult"]
                    ["ApplicationVersions"])

    for version in versions:
        print(version["VersionLabel"])


def list_applications(args):
    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_applications()

    apps = (data['DescribeApplicationsResponse']
                ['DescribeApplicationsResult']
                ['Applications'])

    for app in apps:
        print(app["ApplicationName"])


def list_environments(args):
    if not args.app_name:
        print("Application name required.")
        exit()

    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_environments(application_name=args.app_name)

    envs = (data["DescribeEnvironmentsResponse"]
                ["DescribeEnvironmentsResult"]
                ["Environments"])

    for env_ in envs:
        print(env_["EnvironmentName"])


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.list_envs:
        list_environments(args)
    elif args.app_name:
        list_versions(args)
    else:
        list_applications(args)
