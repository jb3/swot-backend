"""Test the configuration system."""

from pathlib import Path

from attrdict import AttrDict

from backend.config import CONFIG, get_config


def test_get_config() -> None:
    """Test whether the get_config method works as expected."""
    config = get_config()
    assert isinstance(config, AttrDict)


def test_global_config() -> None:
    """Test the global CONFIG instance is okay."""
    assert isinstance(CONFIG, AttrDict)


def test_missing_config() -> None:
    """Test that the expected behaviour occurs when config is missing."""
    new_config_file = Path("config.yaml").rename("../config.yaml")

    config = get_config()
    assert isinstance(config, AttrDict)

    new_config_file.rename("./config.yaml")
