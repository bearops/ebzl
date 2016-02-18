import os
import json
import zipfile
import argparse

from .. lib import (
    parameters
)


DEFAULT_SOURCE_BUNDLE_NAME = "source-bundle.zip"


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl bundle")

    parameters.add_profile(parser, required=False)
    parameters.add_app_name(parser)
    parameters.add_region(parser, required=False)
    parameters.add_version_label(parser, required=False)

    parser.add_argument("-d", "--docker-image",
                        required=True,
                        help="Docker image name.")

    parser.add_argument("--s3-bucket",
                        default="build-deps",
                        help="S3 bucket containing Docker Hub credentials.")

    parser.add_argument("--s3-key",
                        default="generic/docker/.dockercfg",
                        help="S3 key name for Docker Hub credentials file.")

    parser.add_argument("-s", "--source-bundle",
                        default=".",
                        help="Source bundle destination path.")

    parser.add_argument("-x", "--eb-extensions",
                        help=("Path to .ebextensions directory. Its contents "
                              "will be added to the source bundle."))

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
    path = os.path.abspath(os.path.expanduser(args.source_bundle))

    if os.path.isfile(path) and not args.force:
        raise ValueError("Already exists, pass --force to overwrite: %s"
                         % path)
    elif os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return os.path.join(path, DEFAULT_SOURCE_BUNDLE_NAME)

    if not os.path.exists(path):
        dir_ = os.path.dirname(path)
        if not os.path.isdir(dir_):
            raise ValueError("%s does not exist." % dir_)
        return path

    raise NotImplementedError("I have no idea what I'm doing.")


def write_source_bundle(path, dockerrun_contents, eb_extensions_dir):
    if eb_extensions_dir is not None:
        eb_extensions_dir = os.path.expanduser(eb_extensions_dir)

        if not os.path.isdir(eb_extensions_dir):
            raise ValueError(".ebextensions dir doesn't exist: %s"
                             % eb_extensions_dir)

        eb_extensions = [(os.path.join(eb_extensions_dir, fname),
                          ".ebextensions/%s" % fname)
                         for fname in os.listdir(eb_extensions_dir)]
    else:
        eb_extensions = []

    with zipfile.ZipFile(path, "w") as f:
        f.writestr("Dockerrun.aws.json", dockerrun_contents)

        for fpath, arcpath in eb_extensions:
            f.write(fpath, arcpath)


def run(argv):
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv)

    try:
        path = get_source_bundle_file_path(args)
    except ValueError as exc:
        print("Incorrect source bundle path: %s" % exc)
        exit()

    dockerrun_contents = get_docker_run_contents(args)
    write_source_bundle(path, dockerrun_contents, args.eb_extensions)
