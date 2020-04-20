"""Index page for the User API."""
from flask import jsonify, url_for

from backend.database import Session
from backend.models import User
from backend.route import Route


class APIIndex(Route):
    """Index class for the API."""

    name = "index"
    path = "/"

    @staticmethod
    def get() -> str:
        """GET request to the API index."""
        return jsonify({"status": "okay"})
