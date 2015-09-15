from .. lib import eb
import argparse
import subprocess


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl version")

    from .. lib import parameters
    parameters.add_profile(parser, required=False, honour_default=True)
    parameters.add_env_name(parser, required=False)
    parameters.add_region(parser, required=False)

    return parser


def get_git_output(git_command):
    output = subprocess.check_output(git_command, shell=True)
    return filter(lambda x: x, output.split("\n"))[0]


def get_version():
    try:
        get_git_output("git log 2>/dev/null")
    except subprocess.CalledProcessError:
        raise ValueError("Not a git repository.")

    try:
        tag = get_git_output(
            "git describe --exact-match --abbrev=0 2>/dev/null")
    except subprocess.CalledProcessError:
        tag = None

    short_hash = get_git_output(r"git log -1 --pretty=format:%h")

    if tag:
        return "%s-%s" % (tag, short_hash)

    return short_hash


def get_environment_version(args):
    layer1 = eb.get_layer1(profile=args.profile,
                           region=args.region)
    data = layer1.describe_environments(environment_names=[args.env_name])

    envs = (data["DescribeEnvironmentsResponse"]
                ["DescribeEnvironmentsResult"]
                ["Environments"])

    for env_ in envs:
        print(env_["VersionLabel"])


def run(argv):
    from .. lib import parameters
    args = parameters.parse(parser=get_argument_parser(),
                            argv=argv,
                            postprocessors=[parameters.add_default_region])

    if args.env_name:
        get_environment_version(args)
    else:
        try:
            print(get_version())
        except ValueError as exc:
            print("Error: %s" % exc)
