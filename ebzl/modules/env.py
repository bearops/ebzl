import argparse

from .. lib import eb

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
                        help=("AWS region (only needed if the S3 buckets "
                              "needs to be created)."))

    return parser


def env(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        data = layer1.describe_configuration_settings(
            application_name=args.app_name,
            environment_name=args.env_name)
    except boto.exception.BotoServerError as exc:
        print exc.message
        return

    env_vars = (data["DescribeConfigurationSettingsResponse"]
                    ["DescribeConfigurationSettingsResult"]
                    ["ConfigurationSettings"]
                    [0]
                    ["OptionSettings"])

    aws_env_var_option = "aws:elasticbeanstalk:application:environment"

    env_vars = {v["OptionName"]: v["Value"] for v in env_vars
                if v["Namespace"] == aws_env_var_option}

    for key, value in env_vars.iteritems():
        print "%s = %s" % (key, value)


def run(argv):
    args = get_argument_parser().parse_args(argv)

    env(args)
