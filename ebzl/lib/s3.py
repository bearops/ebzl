"""S3 commons."""

import boto

from . import config


def get_connection(profile_name):
    """Get S3 connection for given profile.

    :type profile: basestring
    :rype: boto.s3.connection.S3Connection
    """

    return boto.connect_s3(*config.get_credentials(profile_name))


def map_region_to_location(region):
    """Map AWS region to S3 location.

    :type region: basestring
    """

    if region.startswith("eu-"):
        return "EU"
    return region
