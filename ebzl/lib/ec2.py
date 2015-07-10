"""EC2 commons."""

from . import config

from boto import ec2


def get_region(region_name):
    """Get region info by name.

    :type region_name: basestring
    :rtype: boto.regioninfo.RegionInfo
    """

    for region in ec2.regions():
        if region.name == region_name:
            return region

    raise ValueError("Region not found: %s" % region_name)


def get_connection(profile, region):
    """Get EC2 connection object for given profile & region.

    :type profile: basestring
    :type region: basestring
    :rtype: boto.ec2.connection.EC2Connection
    """

    return ec2.connection.EC2Connection(*config.get_credentials(profile),
                                        region=get_region(region_name=region))
