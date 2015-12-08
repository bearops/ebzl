"""Helper module for parsing AWS ini config files."""

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


AWS_CLI_CREDENTIALS_PATH = "~/.aws/credentials"

AWS_CLI_CONFIG_PATH = "~/.aws/config"

DEFAULT_PROFILE_NAME = os.getenv("AWS_DEFAULT_PROFILE", "default")


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
        raise NoConfigFoundException("Can't find the config file: %s" % path)
    else:
        return config_parser


def _get_credentials_from_environment():
    key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

    return key, secret


def get_credentials(profile=None):
    """Returns AWS credentials.

    Reads ~/.aws/credentials if the profile name is given or tries
    to get them from environment otherwise. Returns a (key, secret)
    tuple.

    :type profile: basestring
    :rtype: tuple
    """

    if profile is None:
        key, secret = _get_credentials_from_environment()

        if key is not None and secret is not None:
            return key, secret

        raise NoConfigFoundException("AWS credentials not found.")

    config = _get_config_parser(path=AWS_CLI_CREDENTIALS_PATH)

    key = config.get(profile, "aws_access_key_id")
    secret = config.get(profile, "aws_secret_access_key")

    return key, secret


def get_credentials_dict(profile):
    """Returns credentials as a dict (for use as kwargs).

    :type profile: basestring
    :rtype: dict
    """

    key, secret = get_credentials(profile)

    return {"aws_access_key_id": key,
            "aws_secret_access_key": secret}


def get_profile_names():
    """Get available profile names.

    :rtype: list
    :returns: list of profile names (strings)
    """

    return _get_config_parser(path=AWS_CLI_CREDENTIALS_PATH).sections()


def has_default_profile():
    """Is default profile present?

    :rtype: bool
    """

    return DEFAULT_PROFILE_NAME in get_profile_names()


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
