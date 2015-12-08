from .. lib import (
    ecs,
    format as fmt,
    parameters
)

from . import (
    version
)

import os
import json
import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser("ebzl ecs")

    parameters.add_profile(parse, required=False)
    parameters.add_region(parser, required=False)

    subparsers = parser.add_subparsers()

    # ebzl ecs create
    create_parser = subparsers.add_parser(
        "create",
        help="register a new task")
    create_parser.set_defaults(func=create_task)
    create_parser.add_argument("--family", required=True)
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--image", required=True)
    create_parser.add_argument("--version", default=version.get_version())
    create_parser.add_argument("--command", default="")
    create_parser.add_argument("--entrypoint", default=[])
    create_parser.add_argument("--cpu", default=0)
    create_parser.add_argument("--memory", default=250)
    create_parser.add_argument("-v", "--var", action="append")
    create_parser.add_argument("-f", "--var-file")

    # ebzl ecs run
    run_parser = subparsers.add_parser(
        "run",
        help="run registered task")
    run_parser.set_defaults(func=run_task)
    run_parser.add_argument("--task", required=True)
    run_parser.add_argument("--cluster", default="default")
    run_parser.add_argument("--command")
    run_parser.add_argument("-v", "--var", action="append")
    run_parser.add_argument("-f", "--var-file")

    # ebzl ecs tasks
    tasks_parser = subparsers.add_parser(
        "tasks",
        help="list available tasks")
    tasks_parser.set_defaults(func=list_tasks)

    # ebzl ecs clusters
    clusters_parser = subparsers.add_parser(
        "clusters",
        help="list available clusters")
    clusters_parser.set_defaults(func=list_clusters)

    return parser


def parse_var_entry(var_entry):
    parts = var_entry.strip().split("=")

    return {"name": parts[0],
            "value": "=".join(parts[1:])}


def parse_var_file(fpath):
    if not fpath or not os.path.isfile(fpath):
        return []

    with open(os.path.expanduser(fpath), "rb") as f:
        return map(parse_var_entry, f.readlines())


def get_env_options(args):
    env_options = []
    env_options.extend(parse_var_file(args.var_file))
    if args.var:
        env_options.extend(map(parse_var_entry, args.var))

    return env_options


def get_container_definition(args):
    return {
        "name": args.name,
        "image": "%s:%s" % (args.image, args.version),
        "mountPoints": [],
        "volumesFrom": [],
        "portMappings": [],
        "command": map(str.strip, args.command.split()),
        "essential": True,
        "entryPoint": args.entrypoint,
        "links": [],
        "cpu": int(args.cpu),
        "memory": int(args.memory),
        "environment": get_env_options(args)
    }


def create_task(args):
    conn = ecs.get_conn(profile=args.profile)

    conn.register_task_definition(
        family="AtlasCron",
        containerDefinitions=[get_container_definition(args)])


def run_task(args):
    conn = ecs.get_conn(profile=args.profile)

    kwargs = {
        "cluster": args.cluster,
        "taskDefinition": args.task,
        "count": 1,
    }

    if args.command or args.var or args.var_file:
        overrides = {}

        task = conn.describe_task_definition(taskDefinition=args.task)
        overrides["name"] = (task["taskDefinition"]
                                 ["containerDefinitions"]
                                 [0]
                                 ["name"])

        if args.command:
            overrides["command"] = map(str.strip, args.command.split())

        env_options = get_env_options(args)
        if env_options:
            overrides["environment"] = env_options

        kwargs["overrides"] = {"containerOverrides": [overrides]}

    print conn.run_task(**kwargs)


def list_tasks(args):
    conn = ecs.get_conn(profile=args.profile)
    tasks = conn.list_task_definitions()
    fmt.print_list([arn.split("/")[-1]
                    for arn in tasks["taskDefinitionArns"]])


def list_clusters(args):
    conn = ecs.get_conn(profile=args.profile)
    clusters = conn.list_clusters()
    fmt.print_list([arn.split("/")[-1]
                    for arn in clusters["clusterArns"]])


def run(argv):
    args = parameters.parse(
        parser=get_argument_parser(),
        argv=argv,
        postprocessors=[parameters.add_default_region])
    args.func(args)
