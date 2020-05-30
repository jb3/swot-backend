"""Test the swot API user index route."""
import json

import pytest
from flask import testing

from app import manager


@pytest.fixture(scope="module")
def client() -> testing.FlaskClient:
    """Create a client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        yield client


def test_api_user_index(client: testing.FlaskClient) -> None:
    """Test the route to render the API user index."""
    resp = client.get("/api/users/")
    data = json.loads(resp.data)

    assert isinstance(data, list)

    if len(data) > 0:
        user = data[0]

        keys = ["email", "full_name", "id", "type", "username"]

        for key in keys:
            assert user.get(key) is not None
