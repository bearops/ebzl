TEXT = "text"

BASH = "bash"

JSON = "json"

DOCKERENV = "dockerenv"

NAME_VALUE_DICT = "nvdict"

DEFAULT = TEXT

CHOICES = (TEXT, BASH, JSON, DOCKERENV, NAME_VALUE_DICT)


def print_dict(dictionary, format_=None):
    """Print a dictionary in a given format. Defaults to text."""

    format_ = format_ or DEFAULT

    if format_ == TEXT:
        for key, value in iter(sorted(dictionary.iteritems())):
            print "%s = %s" % (key, value)
    elif format_ == DOCKERENV:
        for key, value in iter(sorted(dictionary.iteritems())):
            print "%s=%s" % (key, value)
    elif format_ == BASH:
        for key, value in iter(sorted(dictionary.iteritems())):
            print "export %s=%s" % (key, value)
    elif format_ == JSON:
        print json.dumps(dictionary)
    elif format_ == NAME_VALUE_DICT:
        print "["
        for key, value in iter(sorted(dictionary.iteritems())):
            print '{"name": "%s", "value": "%s"},' % (key, value)
        print "]"


def print_list(list_, format_=None):
    """Print a list in a given format. Defaults to text."""

    format_ = format_ or DEFAULT

    if format_ == TEXT:
        for item in list_:
            print item
    elif format_ == JSON:
        print json.dumps(list_)


def print_profile(profile, format_=None):
    """Print profile header."""

    format_ = format_ or DEFAULT

    if format_ == TEXT:
        print "[profile:%s]" % profile
    elif format_ == BASH:
        print "# profile: %s" % profile
