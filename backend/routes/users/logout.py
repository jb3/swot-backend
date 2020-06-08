"""A route to handle logging out users."""

from flask import redirect, Response, session, url_for

from backend.route import Route
from backend.utils import authenticated


class UserLogout(Route):
    """Log users out from swot."""

    name = "logout"
    path = "/logout"

    @authenticated()
    def post(self) -> Response:  # skipcq: PYL-R0201
        """Log users out when they post from the navbar form."""
        # By this point CSRF has been validated so we know this is safe.

        # Pop the user ID from the session, effectively logging them out
        session.pop("uid")

        # Redirect to the home page
        return redirect(url_for("pages.index"))
