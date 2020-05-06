"""Test the route base class is working as expected."""

import pytest
from flask import Blueprint, Flask, testing

from backend.route import Route


class FakeRoute(Route):
    """A fake route used for testing."""

    name = "fake_route"
    path = "/"

    @staticmethod
    def get() -> None:
        """Get request to the route."""
        return "Hello, world!"


class BrokenRoute(Route):
    """A broken route with no name or path set."""

    pass


def create_blueprint() -> Blueprint:
    """Create a blueprint for use in tests."""
    bp = Blueprint("home", __name__)
    FakeRoute.setup(bp)

    return bp


@pytest.fixture(scope="module")
def app() -> Flask:
    """Create a flask app and register the fake route."""
    app = Flask(__name__)
    app.register_blueprint(create_blueprint())

    return app


@pytest.fixture(scope="module")
def client() -> Flask:
    """Create a client for querying flask to emulate a HTTP client."""
    app = Flask(__name__)
    app.register_blueprint(create_blueprint())

    with app.test_client() as client:
        yield client


def test_registered(app: Flask) -> None:
    """Confirm that a route was registered at the home page."""
    for rule in app.url_map.iter_rules():
        assert "GET" in rule.methods
        assert rule.endpoint == "home.fake_route"

        break


def test_get_route(client: testing.FlaskClient) -> None:
    """Confirm that a route can be called."""
    resp = client.get("/")
    assert b"Hello, world!" in resp.data


def test_error_raised_for_invalid_params() -> None:
    """Confirm that when no name or path is given a RuntimeError is raised."""
    bp = Blueprint("home", __name__)

    with pytest.raises(RuntimeError):
        BrokenRoute.setup(bp)
