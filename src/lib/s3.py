import boto

from lib import config


def get_connection(profile_name):
    return boto.connect_s3(*config.get_credentials(profile_name))


def map_region_to_location(region):
    if region.startswith("eu-"):
        return "EU"
    return region

