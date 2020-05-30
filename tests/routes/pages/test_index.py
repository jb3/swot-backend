"""Test the swot index route."""
import pytest
from flask import testing

from app import manager


@pytest.fixture(scope="module")
def client() -> testing.FlaskClient:
    """Create a client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        yield client


def test_pages_index(client: testing.FlaskClient) -> None:
    """Test the route to render the home page for Swot."""
    resp = client.get("/")
    assert "Home • Swot".encode() in resp.data
