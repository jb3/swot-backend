"""A portal for allowing students to see their classes."""

from flask import Response, render_template

from backend.models import UserType
from backend.route import Route
from backend.utils import authenticated


class StudentPortal(Route):
    """A route for displaying student classes."""

    name = "index"
    path = "/"

    @authenticated(user_type=UserType.STUDENT)
    def get(self) -> Response:  # skipcq: PYL-R0201
        """Display a portal page to the user."""
        return render_template("student/index.html")
