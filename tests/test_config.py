"""Test the configuration system."""

from attrdict import AttrDict

from backend.config import CONFIG, get_config


def test_get_config() -> None:
    """Test whether the get_config method works as expected."""
    config = get_config()
    assert isinstance(config, AttrDict)


def test_global_config() -> None:
    """Test the global CONFIG instance is okay."""
    assert isinstance(CONFIG, AttrDict)
