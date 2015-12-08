import argparse

from .. lib import (
    parameters,
    eb,
    ec2,
    format as fmt
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl instances")

    parameters.add_profile(parser, required=False)
    parameters.add_region(parser, required=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--env-name",
                       help="ElasticBeanstalk environment name.")
    group.add_argument("-n", "--name",
                       default="*",
                       help="Instance Name. Wilcards allowed.")

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

    rows = []

    for i in instances:
        rows.append(["%s-%s" % (args.env_name, i.id),
                     "ansible_ssh_host=%s" % i.private_ip_address,
                     "ansible_ssh_user=ec2-user"])

    fmt.print_table(rows, separator=" " * 4)


def instance(args):
    ec2_conn = ec2.get_connection(args.profile, args.region)
    instances = ec2_conn.get_only_instances(filters={"tag:Name": args.name})

    rows = [["NAME", "ID", "IP", "PRIVATE IP", "STACK"]]

    for i in sorted(instances, key=lambda x: x.tags.get("Name", "")):
        if i.state != "running":
            continue

        rows.append([i.tags.get("Name", ""),
                     i.id,
                     i.ip_address or "",
                     i.private_ip_address,
                     i.tags.get("aws:cloudformation:stack-name", "")])

    fmt.print_table(rows)


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.env_name:
        env(args)
    else:
        instance(args)
