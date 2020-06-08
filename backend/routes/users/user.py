"""A portal for managing information about the logged in user."""

from flask import render_template, Response

from backend.route import Route
from backend.utils import authenticated


class UserPortal(Route):
    """A route for displaying a portal with information about the logged in user."""

    name = "user"
    path = "/user"

    @authenticated()
    def get(self) -> Response:  # skipcq: PYL-R0201
        """Display a portal page to the user."""
        return render_template("users/user.html")
