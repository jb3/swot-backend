"""Index page for the User API."""
from flask import jsonify, url_for

from backend.database import Session
from backend.models import User
from backend.route import Route


class UserIndex(Route):
    """Index class for the User API."""

    name = "index"
    path = "/"

    @staticmethod
    def get() -> str:
        """GET request to the User index."""
        sess = Session()

        data = []

        for instance in sess.query(User).order_by(User.id):
            d = instance.__dict__
            d.pop("_sa_instance_state")
            d.pop("password")
            d["goto"] = url_for("api.users.create")
            data.append(d)

        return jsonify(data)
