"""EC2 Container Service commons."""

from . import config

import boto3


def get_conn(profile):
    """Get EC2 Container Service connection object for given profile & region.

    :type profile: basestring
    :type region: basestring
    :rtype: boto.ec2containerservice.layer1.Layer1
    """

    return boto3.client("ecs", **config.get_credentials_dict(profile))
