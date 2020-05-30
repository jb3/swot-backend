"""Test the swot API indexroute."""
import json

import pytest
from flask import testing

from app import manager


@pytest.fixture(scope="module")
def client() -> testing.FlaskClient:
    """Create a client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        yield client


def test_api_index(client: testing.FlaskClient) -> None:
    """Test the route to render the API index."""
    resp = client.get("/api/")
    data = json.loads(resp.data)

    assert data["status"] == "okay"
