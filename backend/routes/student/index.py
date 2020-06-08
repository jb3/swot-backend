"""A portal for allowing students to see their classes."""

from flask import render_template, Response

from backend.route import Route
from backend.utils import authenticated


class StudentPortal(Route):
    """A route for displaying student classes."""

    name = "index"
    path = "/"

    @authenticated(user_type="student")  # skipcq: PYL-R0201
    def get(self) -> Response:
        """Display a portal page to the user."""
        return render_template("student/index.html")
