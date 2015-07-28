# Change log

## 2015-07-28
- set environment variables with `ebzl env --var-file PATH`

## 2015-07-26
- set environment variables with `ebzl env -v FOO=BAR`

## 2015-07-21
- `bundle` bug fixes

## 2015-07-09
- added ebzl to PyPi: https://pypi.python.org/pypi/ebzl
- don't require `--app-name` in `env` & `instances` anymore
- Python 3 compatibility

## 2015-07-08
- `instances`: get EC2 instances by name with `ebzl instances -n InstanceName`,
  displays instance id, public and private IP (if exists)

## 2015-06-28
- ported `--format` feature from ebizzle.
- `--region` is not required anymore, ebzl will try to determine it based on
  `~/.aws/config` and quit with an error message if fails
- common helpers for parameters handling
- added a change log
