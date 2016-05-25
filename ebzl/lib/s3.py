"""S3 commons."""

import boto

from . import config


def get_connection(profile_name, region):
    """Get S3 connection for given profile.

    :type profile: basestring
    :rype: boto.s3.connection.S3Connection
    """

    return boto.connect_s3(*config.get_credentials(profile_name),
                           host="s3.%s.amazonaws.com" % region)


def map_region_to_location(region):
    """Map AWS region to S3 location.

    :type region: basestring
    """

    s3_locations = {
        "APNortheast",
        "APSoutheast",
        "APSoutheast2",
        "DEFAULT",
        "EU",
        "EUCentral1",
        "SAEast",
        "USWest",
        "USWest2"
    }

    for location in s3_locations:
        if location.lower() == "".join(region.lower().split("-")):
            return location

    raise NotImplementedError("Boo hoo.")

