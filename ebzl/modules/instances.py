import argparse

from .. lib import (
    parameters,
    eb,
    ec2
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl instances")
    
    parameters.add_profile(parser)
    parameters.add_app_name(parser)
    parameters.add_region(parser, required=False)

    parser.add_argument("-e", "--env-name",
                        required=True,
                        help="ElasticBeanstalk environment name.")

    return parser


def env(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        data = layer1.describe_environment_resources(
            environment_name=args.env_name)
    except boto.exception.BotoServerError as exc:
        print exc.message
        return

    instance_ids = (data["DescribeEnvironmentResourcesResponse"]
                        ["DescribeEnvironmentResourcesResult"]
                        ["EnvironmentResources"]
                        ["Instances"])

    instance_ids = [x["Id"] for x in instance_ids]

    ec2_conn = ec2.get_connection(args.profile, args.region)
    instances = ec2_conn.get_only_instances(instance_ids=instance_ids)

    for i in instances:
        print "%s-%s\tansible_ssh_host=%s\tansible_ssh_user=ec2-user" % (
            args.app_name, i.id, i.private_ip_address)


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    env(args)
