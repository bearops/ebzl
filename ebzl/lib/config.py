import os
import ConfigParser


class NoConfigFoundException(Exception):
    pass


def _get_config_parser(path):
    config_parser = ConfigParser.ConfigParser()

    try:
        with open(os.path.expanduser(path), "rb") as f:
            config_parser.readfp(f)
    except IOError:
        return None
    else:
        return config_parser


def _get_credentials_data():
    """Return ebizzle's config."""

    config_paths = [
        "~/.aws/credentials"
    ]

    for config_path in config_paths:
        config_parser = _get_config_parser(config_path)
        if config_parser is not None:
            return config_parser
    raise NoConfigFoundException(
        "Can't find a config file in any of the locations: %s"
        % config_paths)


def _get_config_data(config_path="~/.aws/config"):
    parser = _get_config_parser(config_path)

    if parser is not None:
        return parser

    raise NoConfigFoundException("Can't find the config file: %s" 
                                 % config_path)


def get_credentials(profile):
    """Returns credentials for given profile as a (key, secret) tuple."""

    config = _get_credentials_data()

    key = config.get(profile, "aws_access_key_id")
    secret = config.get(profile, "aws_secret_access_key")

    return key, secret


def get_profile_names():
    """Get available profile names."""

    return _get_credentials_data().sections()


def get_default_region(profile):
    """Get the default region for given profile from AWS CLI tool's config."""

    config = _get_config_data()

    try:
        return config.get("profile %s" % profile, "region")
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        pass

    try:
        return config.get("default", "region")
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        pass

    return None
