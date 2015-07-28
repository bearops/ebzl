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
    parameters.add_region(parser, required=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--env-name",
                       help="ElasticBeanstalk environment name.")
    group.add_argument("-n", "--name",
                       help="Instance Name (tag).")

    return parser


def env(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        data = layer1.describe_environment_resources(
            environment_name=args.env_name)
    except boto.exception.BotoServerError as exc:
        print(exc.message)
        return

    instance_ids = (data["DescribeEnvironmentResourcesResponse"]
                        ["DescribeEnvironmentResourcesResult"]
                        ["EnvironmentResources"]
                        ["Instances"])

    instance_ids = [x["Id"] for x in instance_ids]

    ec2_conn = ec2.get_connection(args.profile, args.region)
    instances = ec2_conn.get_only_instances(instance_ids=instance_ids)

    for i in instances:
        print("%s-%s\tansible_ssh_host=%s\tansible_ssh_user=ec2-user" % (
            args.env_name, i.id, i.private_ip_address))


def instance(args):
    ec2_conn = ec2.get_connection(args.profile, args.region)
    instances = ec2_conn.get_only_instances(filters={"tag:Name": args.name})

    for i in instances:
        if i.state != "running":
            continue

        i.ip_address = i.ip_address or ""

        print("%s %s %s" % (i.id,
                            i.ip_address.center(15),
                            i.private_ip_address.center(15)))


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.env_name:
        env(args)
    else:
        instance(args)
