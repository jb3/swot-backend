"""A portal for managing information about the logged in user."""

from flask import g, Response, render_template, session

from backend.route import Route
from backend.utils import authenticated


class UserPortal(Route):
    """A route for displaying a portal with information about the logged in user."""

    name = "user"
    path = "/user"

    @staticmethod
    @authenticated
    def get() -> Response:
        """Display a portal page to the user."""
        return render_template("users/user.html", user=g.user)
