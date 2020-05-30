"""Test the user creation route."""
import pytest
from flask import testing

from app import manager


@pytest.fixture(scope="module")
def client() -> testing.FlaskClient:
    """Create a client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        yield client


def test_sign_up_get(client: testing.FlaskClient) -> None:
    """Test the route to render the user sign up page."""
    resp = client.get("/users/sign_up")
    assert "Sign up • Swot".encode() in resp.data
