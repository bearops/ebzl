import os
import json
import zipfile
import argparse

from .. lib import (
    eb,
    s3
)

import boto


DEFAULT_SOURCE_BUNDLE_NAME = "source-bundle.zip"


def get_argument_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Force, overwrite & burn things in the process.")
    
    parser.add_argument("-d", "--docker-image",
                        default=True,
                        help="Docker image name.")

    parser.add_argument("-v", "--version",
                        required=True,
                        help="Version label.")


    parser.add_argument("--s3-bucket",
                        default="build-deps",
                        help="AWS S3 bucket containing Docker Hub credentials.")

    parser.add_argument("--s3-key",
                        default="generic/docker/.dockercfg",
                        help="AWS S3 key name for Docker Hub credentials file.")

    parser.add_argument("-s", "--source-bundle",
                        default=".",
                        help="Source bundle destination path.")

    return parser


def get_docker_run_contents(args):
    data = {
        "AWSEBDockerrunVersion": "1",
        "Image": {
            "Name": "%s:%s" % (args.docker_image, args.version),
            "Update": "true"
        },
        "Authentication": {
            "Bucket": args.s3_bucket,
            "Key": args.s3_key
        },
        "Ports": [{
             "ContainerPort": "80"
        }],
        "Logging": "/home/dubizzle/logs/user"
    }

    return json.dumps(data, indent=4)


def get_source_bundle_file_path(args):
    path = args.source_bundle

    if os.path.isfile(path) and not args.force:
        raise ValueError("Already exists, pass --force to overwrite: %s" % path)
    
    elif os.path.isfile(path):
        return path
       
    elif os.path.isdir(path):
        return os.path.join(os.path.expanduser(path), 
                            DEFAULT_SOURCE_BUNDLE_NAME)
    
    if not os.path.exists(path):
        dir_ = os.path.dirname(path)
        if not os.path.isdir(dir_):
            raise ValueError("%s does not exist." % dir_)
        return path

    raise NotImplementedError("I have no idea what I'm doing.")


def write_source_bundle(path, dockerrun_contents):
    with zipfile.ZipFile(path, "w") as f:
        f.writestr("Dockerrun.aws.json", dockerrun_contents)


def run(argv):
    args = get_argument_parser().parse_args(argv)

    try: 
        path = get_source_bundle_file_path(args)
    except ValueError as exc:
        print "Incorrect source bunde path: %s" % exc
        exit()

    dockerrun_contents = get_docker_run_contents(args)

    write_source_bundle(path, dockerrun_contents)
   

