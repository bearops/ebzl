# coding: utf-8
import argparse

from .. lib import (
    eb,
    parameters
)

import boto


EB_ENV = "aws:elasticbeanstalk:application:environment"


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl env")

    parameters.add_profile(parser)
    parameters.add_region(parser, required=False)

    parser.add_argument("-e", "--env-name",
                        required=True,
                        help="ElasticBeanstalk environment name.")

    parser.add_argument("-v", "--var",
                        required=False,
                        action="append",
                        help="Variable to set, format: -v Key=Value.")

    return parser


def get_env(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        data = layer1.describe_configuration_settings(
            application_name=None,
            environment_name=args.env_name)
    except boto.exception.BotoServerError as exc:
        print(exc.message)
        return

    env_vars = (data["DescribeConfigurationSettingsResponse"]
                    ["DescribeConfigurationSettingsResult"]
                    ["ConfigurationSettings"]
                    [0]
                    ["OptionSettings"])

    aws_env_var_option = "aws:elasticbeanstalk:application:environment"

    env_vars = {v["OptionName"]: v["Value"] for v in env_vars
                if v["Namespace"] == aws_env_var_option}

    return env_vars


def env(args):
    env_vars = get_env(args)

    for key, value in env_vars.items():
        print("%s := %s" % (key, value))


def env_set(args):
    current_vars = get_env(args)

    option_settings = []
    skip_option_settings = []

    for var in args.var:
        parts = var.split("=")
        entry = (EB_ENV, parts[0], "=".join(parts[1:]))

        if current_vars.get(entry[1], None) == entry[2]:
            skip_option_settings.append(entry)
        else:
            option_settings.append(entry)

    if option_settings:
        print "UPDATE:"
        for t, k, v in option_settings:
            print "  %s = %s" % (k, v)

    if skip_option_settings:
        print "SKIP:"
        for t, k, v in skip_option_settings:
            print "  %s = %s" % (k, v)

    if not option_settings:
        print "There's nothing to update."
        return

    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    try:
        data = layer1.update_environment(environment_name=args.env_name,
                                         option_settings=option_settings)
    except boto.exception.BotoServerError as exc:
        print(exc.message)
        return


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.var:
        env_set(args)
    else:
        env(args)
