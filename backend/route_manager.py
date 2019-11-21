"""Manage routes for application."""
import glob
import importlib
import inspect

from flask import Blueprint, Flask, Response

from .config import CONFIG
from .mappings import MAPPINGS
from .route import Route


class RouteManager:
    """Class to manage routes for the flask application."""

    def __init__(self: "RouteManager") -> None:
        """Initialise a new route manager and with it a flask application."""
        self.app = Flask(__name__)

        self.app.config.from_object(dict(CONFIG.flask))

        self.app.after_request(self.after_request)

        self.load_routes()

    def run(self: "RouteManager") -> None:
        """Start the flask application."""
        self.app.run()

    @staticmethod
    def after_request(response: Response) -> Response:
        """Process a response before it is sent to the client."""
        if "text/html" in response.headers["Content-Type"]:
            response.headers["Content-Type"] = "text/plain"

        return response

    def load_routes(self: "RouteManager") -> None:
        """Load the routes from the route directories."""
        for bp_name, path in MAPPINGS.items():
            bp = Blueprint(bp_name, bp_name)

            for file in glob.glob(f"backend/routes/{bp_name}/*.py"):
                imp = file[:-3].replace("/", ".")

                module = importlib.import_module(imp)

                for _, member in inspect.getmembers(module):
                    if (inspect.isclass(member)
                        and Route in member.__mro__
                        and member is not Route
                        ):  # noqa
                        member.setup(self, bp)

            self.app.register_blueprint(bp, url_prefix=path)
