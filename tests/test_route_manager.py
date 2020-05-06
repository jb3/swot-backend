"""Test the Route manager."""

import pytest
from flask import Response

from backend.route_manager import RouteManager


@pytest.fixture(scope="module")
def route_manager() -> RouteManager:
    """Create a dummy route manager."""
    return RouteManager()


def test_create_route_manager(route_manager: RouteManager) -> None:
    """Create a new route manager."""
    assert isinstance(route_manager, RouteManager)


def test_after_request(route_manager: RouteManager) -> None:
    """Check the after_request callback works."""
    resp = Response("Hello, world!")

    route_manager.after_request(resp)
