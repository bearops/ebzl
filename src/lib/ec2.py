from lib import config

import boto
from boto import ec2


def get_region(region_name):
    for region in ec2.regions():
        if region.name == region_name:
            return region

    raise ValueError("Region not found: %s" % region_name)


def get_connection(profile, region):
    return ec2.connection.EC2Connection(*config.get_credentials(profile),
                                        region=get_region(region_name=region))

