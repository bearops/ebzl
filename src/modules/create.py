import os
import argparse

from lib import (
    eb,
    s3
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

    parser.add_argument("-v", "--version",
                        required=True,
                        help="Version label.")

    parser.add_argument("-s", "--source-bundle",
                        required=True,
                        help="ElasticBeanstalk source bundle archive.")

    parser.add_argument("--s3-bucket",
                        help="Source bundle destination AWS S3 bucket.")

    parser.add_argument("-r", "--region",
                        required=True,
                        help="AWS region (only needed if the S3 buckets needs to be created).")

    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Force, overwrite & burn things in the process.")

    return parser


def get_source_bundle_key_name(app_name, version):
    return "%s/%s.zip" % (app_name, version)


def upload_source_bundle(args):
    source_bundle_path = os.path.expanduser(args.source_bundle)

    s3_conn = s3.get_connection(profile_name=args.profile)

    try:
        bucket = s3_conn.get_bucket(args.s3_bucket)
    except boto.exception.S3ResponseError as e:
        print "S3 bucket not found, creating: %s" % args.s3_bucket
        bucket = s3_conn.create_bucket(
            args.s3_bucket, 
            location=s3.map_region_to_location(args.region))

    key = boto.s3.key.Key(
        bucket, 
        get_source_bundle_key_name(args.app_name, args.version))

    if key.exists() and not args.force:
        print "Key already exists: %s (pass --force to overwrite)" % key.name
        exit()
    
    with open(source_bundle_path, "rb") as f:
        key.set_contents_from_file(f)

    return key.key


def create_eb_version(args):
    layer1 = eb.get_layer1(profile=args.profile, region=args.region)

    kwargs = {
        "application_name": args.app_name,
        "version_label": args.version,
        "description": args.version,
        "s3_bucket": args.s3_bucket,
        "s3_key": get_source_bundle_key_name(args.app_name, 
                                             args.version)
    }

    try:
        layer1.create_application_version(**kwargs)
    except boto.exception.BotoServerError as exc:
        print exc.message
        exit()
    

def run(argv):
    args = get_argument_parser().parse_args(argv)

    upload_source_bundle(args)
    create_eb_version(args)

