"""ElasticBeanstalk commons."""

from . import config

from boto import beanstalk
from boto.beanstalk import layer1


def get_region(region_name):
    """Get region info by name.

    :type region_name: basestring
    :rtype: boto.regioninfo.RegionInfo
    """

    for beanstalk_region in beanstalk.regions():
        if beanstalk_region.name == region_name:
            return beanstalk_region

    raise ValueError("Region not found: %s" % region_name)


def get_layer1(profile, region):
    """Get Beanstalk connection object for given profile & region.

    :type profile: basestring
    :type region: basestring
    :rtype: boto.beanstalk.layer1.Layer1
    """

    return layer1.Layer1(*config.get_credentials(profile),
                         region=get_region(region))
