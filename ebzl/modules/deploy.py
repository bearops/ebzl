from ..lib import eb
import argparse
import boto


def get_argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--env-name", 
                        required=True, 
                        help="ElasticBeanstalk environment name.")

    parser.add_argument("-v", "--version",
                        required=True,
                        help="Version label.")

    parser.add_argument("-p", "--profile",
                        required=True,
                        help="AWS credentials profile.")

    parser.add_argument("-r", "--region",
                        required=True,
                        help="AWS region (only needed if the S3 buckets needs to be created).")
    
    return parser


def deploy(args):
    kwargs = {
        "environment_name": args.env_name,
        "version_label": args.version
    }
    
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)
    
    try:
        layer1.update_environment(**kwargs)
    except boto.exception.BotoServerError as exc:
        print exc.message


def run(argv):
    args = get_argument_parser().parse_args(argv)

    deploy(args)
