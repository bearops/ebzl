# ebzl

A helper tool for easier AWS ElasticBeanstalk applications and environments management.

# Install

```bash
pip install ebzl
```

# Config

`ebzl` will read AWS credentials from `$HOME/.aws/credentials` and region defaults from `$HOME/.aws/config`.

# Usage

```bash
ebzl help
```

## Modules

- `bundle`: create and upload Beanstalk source bundle for Docker deployments.
- `create`: create Beanstalk application version.
- `delete`: delete Beanstalk application version.
- `deploy`: deploy a version to given Beanstalk environment.
- `ecs`: register, run & list EC2 Container Service tasks.
- `env`: read and write environment variables of a given Beanstalk environment.
- `help`: provide help on _ebzl_ usage.
- `instances`: list instances for given Beanstalk environment or matching a name pattern.
- `list`: list available Beanstalk applications, environments and versions.
- `version`: get project's or Beanstalk environment version.

# License

We're using BSD-3. Please refer to [the license file](https://github.com/bearops/ebzl/blob/master/LICENSE) for details.
