"""Test the mappings file."""

from backend.mappings import MAPPINGS


def test_mappings_type() -> None:
    """Assert mappings is a dictionary."""
    assert isinstance(MAPPINGS, dict)


def test_mappings_root() -> None:
    """Assert the home mapping points to pages."""
    assert MAPPINGS["/"] == "pages"