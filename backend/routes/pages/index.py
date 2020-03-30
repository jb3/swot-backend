"""Index page for the User API."""
from backend.route import Route

class PageIndex(Route):
    """Index class for Swot"""

    name = "index"
    path = "/"

    @staticmethod
    def get() -> str:
        """GET request to the Page index."""

        return "Hello world!"
