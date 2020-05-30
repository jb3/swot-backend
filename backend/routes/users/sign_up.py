"""Route for signing up for Swot."""
from flask import render_template

from backend.route import Route


class UserSignUp(Route):
    """Route for signing up for Swot."""

    name = "sign_up"
    path = "/sign_up"

    @staticmethod
    def get() -> str:
        """GET request to the Page index."""
        # Render the user creation page
        return render_template("users/create.html")
