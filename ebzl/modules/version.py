import argparse
import subprocess

def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl version")

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
        tag = get_git_output("git describe --exact-match --abbrev=0 2>/dev/null")
    except subprocess.CalledProcessError:
        tag = None

    short_hash = get_git_output(r"git log -1 --pretty=format:%h")

    if tag:
        return "%s-%s" % (tag, short_hash)

    return short_hash


def run(argv):
    try:
        print get_version()
    except ValueError as exc:
        print "Error: %s" % exc


