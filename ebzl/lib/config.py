"""Helper module for parsing AWS ini config files."""

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


AWS_CLI_CREDENTIALS_PATH = "~/.aws/credentials"

AWS_CLI_CONFIG_PATH = "~/.aws/config"


class NoConfigFoundException(Exception):
    """Config file not present."""

    pass


def _get_config_parser(path):
    """Open and parse given config.

    :type path: basestring
    :rtype: ConfigParser.ConfigParser
    """

    config_parser = configparser.ConfigParser()

    try:
        with open(os.path.expanduser(path), "rb") as f:
            config_parser.readfp(f)
    except IOError:
        raise NoConfigFoundException(
            "Can't find the config file: %s"
            % config_paths)
    else:
        return config_parser


def get_credentials(profile):
    """Returns credentials for given profile as a (key, secret) tuple.

    :type profile: basestring
    :rtype: tuple
    """

    config = _get_config_parser(path=AWS_CLI_CREDENTIALS_PATH)

    key = config.get(profile, "aws_access_key_id")
    secret = config.get(profile, "aws_secret_access_key")

    return key, secret


def get_profile_names():
    """Get available profile names.

    :rtype: list
    :returns: list of profile names (strings)
    """

    return _get_config_parser(path=AWS_CLI_CREDENTIALS_PATH).sections()


def get_default_region(profile):
    """Get the default region for given profile from AWS CLI tool's config.

    :type profile: basestring
    :rtype: basestring
    :returns: name of defalt region if defined in config, None otherwise
    """

    config = _get_config_parser(path=AWS_CLI_CONFIG_PATH)

    try:
        return config.get("profile %s" % profile, "region")
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass

    try:
        return config.get("default", "region")
    except (configparser.NoSectionError, configparser.NoOptionError):
        pass

    return None
