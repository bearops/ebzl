import os
import argparse

from .. lib import (
    eb,
    s3,
    parameters
)

import boto


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl create")

    parameters.add_profile(parser, required=False)
    parameters.add_app_name(parser)
    parameters.add_version_label(parser, required=False)
    parameters.add_region(parser, required=False)
    parameters.add_force(parser)

    parser.add_argument("-s", "--source-bundle",
                        required=True,
                        help="ElasticBeanstalk source bundle archive.")

    parser.add_argument("--s3-bucket",
                        required=True,
                        help="Source bundle destination AWS S3 bucket.")

    return parser


def get_source_bundle_key_name(app_name, version):
    return "%s/%s.zip" % (app_name, version)


def upload_source_bundle(args):
    source_bundle_path = os.path.expanduser(args.source_bundle)

    s3_conn = s3.get_connection(profile_name=args.profile, region=args.region)

    try:
        bucket = s3_conn.get_bucket(args.s3_bucket)
    except boto.exception.S3ResponseError:
        print("S3 bucket not found, creating: %s" % args.s3_bucket)
        bucket = s3_conn.create_bucket(
            args.s3_bucket,
            location=s3.map_region_to_location(args.region))

    key = boto.s3.key.Key(
        bucket,
        get_source_bundle_key_name(args.app_name, args.version))

    if key.exists() and not args.force:
        print("Key already exists: %s (pass --force to overwrite)" % key.name)
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
        print(exc.message)
        exit()


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    upload_source_bundle(args)
    create_eb_version(args)
