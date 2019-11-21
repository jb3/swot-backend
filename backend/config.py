"""Configuration system for Swot Backend."""
import yaml
from attrdict import AttrDict


def get_config() -> AttrDict:
    """Fetch the configuration from the YAML file."""
    with open("config.yaml") as config:
        conf = yaml.safe_load(config)

        return AttrDict(conf)


CONFIG = get_config()
