"""Configuration system for Swot Backend."""
from pathlib import Path

import yaml
from attrdict import AttrDict


def get_config() -> AttrDict:
    """Fetch the configuration from the YAML file."""
    if Path("config.yaml").exists():
        config_path = "config.yaml"
    else:
        print("WARNING: No config set, defaulting to config-example.yaml")
        print("WARNING: To get rid of this warning, copy config-example.yaml")
        print("WARNING: to a new file called config.yaml and edit")
        config_path = "config-example.yaml"

    # Open the config file
    with open(config_path) as config:
        # Parse the YAML to a python dictionary
        conf = yaml.safe_load(config)

        # Convert the dictionary into a class using attributes
        # so instead of config["db"]["host"] one can run
        # config.db.host
        return AttrDict(conf)


# Create a global config object that can be imported
CONFIG = get_config()
