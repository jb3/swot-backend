"""A portal for allowing teachers to see all classes."""

from flask import render_template, Response

from backend.route import Route
from backend.utils import authenticated


class TeacherPortal(Route):
    """A route for displaying classes."""

    name = "index"
    path = "/"

    @staticmethod
    @authenticated(user_type="teacher")
    def get() -> Response:
        """Display a portal page to the user."""
        return render_template("teacher/index.html")
