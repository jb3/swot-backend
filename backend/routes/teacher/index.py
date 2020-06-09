"""A portal for allowing teachers to see all classes."""

from flask import Response, render_template

from backend.models import UserType
from backend.route import Route
from backend.utils import authenticated


class TeacherPortal(Route):
    """A route for displaying classes."""

    name = "index"
    path = "/"

    @authenticated(user_type=UserType.TEACHER)
    def get(self) -> Response:  # skipcq: PYL-R0201
        """Display a portal page to the user."""
        return render_template("teacher/index.html")
