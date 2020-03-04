"""Index page for the User API."""
from backend.route import Route


class UserIndex(Route):
    """Index class for the User API."""

    name = "index"
    path = "/"

    def get(self: "UserIndex") -> str:
        """GET request to the User index."""
        return "Index for User API"
