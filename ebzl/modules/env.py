import argparse

from .. lib import (
    eb,
    parameters
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl env")
    
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
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])
    
    env(args)
