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

| Module | Description |
| -------- | -------------------------------------- |
| `bundle` | Create and upload Beanstalk source bundle for Docker deployments. |
| `create` | Create Beanstalk application version. |
| `delete` | Delete Beanstalk application version. |
| `deploy` | Deploy a version to given Beanstalk environment. |
| `ecs` | Register, run & list EC2 Container Service tasks. |
| `env` | Read and write environment variables of a given Beanstalk environment. |
| `help` | Provide help on _ebzl_ usage. |
| `instances` | List instances for given Beanstalk environment or matching a name pattern. |
| `list` | List available Beanstalk applications, environments and versions. |
| `version` | Get project's or Beanstalk environment version. |

# License

We're using BSD-3. Please refer to [the license file](LICENSE) for details.
