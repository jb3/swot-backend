"""About page for Swot."""
from flask import render_template

from backend.route import Route


class PageAbout(Route):
    """About class for Swot."""

    name = "about"
    path = "/about"

    @staticmethod
    def get() -> str:
        """GET request to the about page."""
        return render_template("pages/about.html")  # Render the index template
