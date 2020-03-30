"""Manage routes for application."""
import glob
import importlib
import inspect
import typing

from flask import Blueprint, Flask, Response

from .config import CONFIG
from .database import connect
from .mappings import MAPPINGS
from .route import Route


class RouteManager:
    """Class to manage routes for the flask application."""

    def __init__(self: "RouteManager") -> None:
        """Initialise a new route manager and with it a flask application."""
        self.app = Flask(__name__, root_path="backend/")

        self.app.config.from_object(dict(CONFIG.flask))

        self.app.after_request(self.after_request)

        self.db = connect()

        self.load_routes()

    def run(self: "RouteManager") -> None:
        """Start the flask application."""
        self.app.run(
            host=CONFIG.host.host,
            port=CONFIG.host.port,
            debug=CONFIG.host.debug,
        )

    @staticmethod
    def after_request(response: Response) -> Response:
        """Process a response before it is sent to the client."""
        # if "text/html" in response.headers["Content-Type"]:
        #    response.headers["Content-Type"] = "text/plain"

        return response

    def load_from_key_or_recurse(
        self: "RouteManager",
        namespace: str,
        bp_name: str,
        data: typing.Union[dict, str]
    ):
        """
        The mapping file may specify an area as either a string for the route
        or a dictionary which should be recursed into. This function either
        loads the blueprint or steps down into the dictionary.
        """
        if isinstance(data, str):
            bp = Blueprint(bp_name, __name__)

            print(f"{namespace}{data}")

            for file in glob.glob(f"backend/routes/{namespace}{data}/*.py"):
                print(file)
                imp = file[:-3].replace("/", ".")

                module = importlib.import_module(imp)

                for _, member in inspect.getmembers(module):
                    if (
                        inspect.isclass(member)
                        and Route in member.__mro__
                        and member is not Route
                    ):  # noqa
                        member.setup(self, bp)

            self.app.register_blueprint(bp, url_prefix="/" + bp_name.replace(".", "/"))
        else:
            for key, val in data.items():
                print(key, val)
                self.load_from_key_or_recurse(
                    f"{namespace}{bp_name}/",
                    f"{bp_name}.{key.replace('/', '')}",
                    val
                )

    def load_routes(self: "RouteManager") -> None:
        """Load the routes from the route directories."""
        for bp_name, path in MAPPINGS.items():
            self.load_from_key_or_recurse("", bp_name, path)