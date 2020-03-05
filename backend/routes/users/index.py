"""Index page for the User API."""
from backend.database import Session
from backend.route import Route
from backend.models import User

from flask import jsonify

class UserIndex(Route):
    """Index class for the User API."""

    name = "index"
    path = "/"

    def get(self: "UserIndex") -> str:
        """GET request to the User index."""
        sess = Session()

        data = []

        for instance in sess.query(User).order_by(User.id):
            d = instance.__dict__
            d.pop("_sa_instance_state")
            data.append(d)

        return jsonify(data)
