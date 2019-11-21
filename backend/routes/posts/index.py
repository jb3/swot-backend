"""Index page for the Post API."""
from backend.route import Route


class PostIndex(Route):
    """Index class for the Post API."""

    name = "index"
    path = "/"

    def get(self: "PostIndex") -> str:
        """GET request to the Post index."""
        return "Index for Post API"
