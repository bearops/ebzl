from lib import eb
import argparse
import boto


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--app-name", 
                        required=False, 
                        help="ElasticBeanstalk application name.")
    
    parser.add_argument("-p", "--profile",
                        required=True,
                        help="AWS credentials profile.")
    
    parser.add_argument("-r", "--region",
                        required=True,
                        help="AWS region (only needed if the S3 buckets needs to be created).")

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
    args = get_argument_parser().parse_args(argv)

    if args.app_name:
        list_versions(args)
    else:
        list_applications(args)

