"""Configuration system for Swot Backend."""
import yaml
from attrdict import AttrDict


def get_config() -> AttrDict:
    """Fetch the configuration from the YAML file."""
    # Open the config.yaml file
    with open("config.yaml") as config:
        # Parse the YAML to a python dictionary
        conf = yaml.safe_load(config)

        # Convert the dictionary into a class using attributes
        # so instead of config["db"]["host"] one can run
        # config.db.host
        return AttrDict(conf)


# Create a global config object that can be imported
CONFIG = get_config()
