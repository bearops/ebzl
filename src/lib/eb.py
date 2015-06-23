from lib import config

from boto import beanstalk
from boto.beanstalk import layer1


def get_region(region_name):
    for beanstalk_region in beanstalk.regions():
        if beanstalk_region.name == region_name:
            return beanstalk_region

    raise ValueError("Region not found: %s" % region_name)


def get_layer1(profile, region):
    return layer1.Layer1(*config.get_credentials(profile), 
                         region=get_region(region))

