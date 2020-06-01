"""Test utility functions."""

from backend import utils


def test_code_generator() -> None:
    """Test that class code generation works."""
    assert len(utils.code_generate(k=10)) == 10

    assert len(utils.code_generate(k=5)) == 5
