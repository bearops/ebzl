import os
import ConfigParser


DEFAULT_PROFILE = "test"

_profiles = [DEFAULT_PROFILE]


class NoConfigFoundException(Exception):
    pass


def set_profiles(profiles):
    for profile in profiles:
        assert profile in get_profile_names()

    global _profiles
    _profiles = profiles


def get_profiles():
    return _profiles


def _get_config_parser():
    """Return ebizzle's config."""

    config_paths = [
        "~/.aws/credentials",
        "~/.ebizzle/config"
    ]

    for config_path in config_paths:
        if os.path.isfile(os.path.expanduser(config_path)):
            config_parser = ConfigParser.ConfigParser()
            config_parser.read(os.path.expanduser(config_path))
            break
    else:
        raise NoConfigFoundException(
            "Can't find a config file in any of the locations: %s"
            % config_paths)

    return config_parser


def get_credentials(profile):
    """Returns credentials for given profile as a (key, secret) tuple."""

    config = _get_config_parser()

    key = config.get(profile, "aws_access_key_id")
    secret = config.get(profile, "aws_secret_access_key")

    return key, secret


def get_profile_names():
    """Get available profile names."""

    return _get_config_parser().sections()

