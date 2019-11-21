"""Configuration system for Swot Backend."""

from attrdict import AttrDict
import yaml


def get_config() -> AttrDict:
    """Fetch the configuration from the YAML file."""
    with open("config.yaml") as config:
        conf = yaml.load(config)

        return AttrDict(conf)


CONFIG = get_config()
