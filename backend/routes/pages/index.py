"""Index page for the User API."""
from flask import render_template

from backend.route import Route


class PageIndex(Route):
    """Index class for Swot."""

    name = "index"
    path = "/"

    @staticmethod
    def get() -> str:
        """GET request to the Page index."""
        return render_template("pages/index.html")  # Render the index template
