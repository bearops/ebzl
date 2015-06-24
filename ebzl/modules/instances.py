import argparse

from ..lib import (
    eb,
    ec2
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--profile",
                        required=True,
                        help="AWS credentials profile.")
    
    parser.add_argument("-a", "--app-name", 
                        required=True, 
                        help="ElasticBeanstalk application name.")
    
    parser.add_argument("-e", "--env-name", 
                        required=True, 
                        help="ElasticBeanstalk environment name.")

    parser.add_argument("-r", "--region",
                        required=True,
                        help="AWS region (only needed if the S3 buckets needs to be created).")

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
    args = get_argument_parser().parse_args(argv)

    env(args)
