# Change log

## 2015-07-08
- instances: get EC2 instances by name with `ebzl instances -n InstanceName`,
  displays instance id, public and private IP (if exists)

## 2015-06-28
- Ported format feature from ebizzle.
- Region parameter is not required anymore, ebzl will try to determine it based on
  `~/.aws/config` and quit with an error message if fails.
- Common helpers for parameters handling.
- Added a change log.
