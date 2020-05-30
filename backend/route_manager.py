"""Manage routes for application."""
import glob
import importlib
import inspect
import typing
from pathlib import Path

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

        # Since we do not have the static folder in the default location,
        # create a path here pointing to backend/static
        self.app._static_folder = str(Path.cwd() / "backend" / "static")

        # Update the flask configuration from the custom config file
        self.app.config.from_object(dict(CONFIG.flask))

        # Register the after_request hook with flask to run a function
        # after every request
        self.app.after_request(self.after_request)

        # Create an app instance of the DB
        self.db = connect()

        # Load all the routes
        self.load_routes()

    def run(self: "RouteManager") -> None:
        """Start the flask application."""
        # Start the web application on the parameters provided in YAML
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
    ) -> None:
        """
        Load a mapping file or recurse into a directory.

        The mapping file may specify an area as either a string for the route
        or a dictionary which should be recursed into. This function either
        loads the blueprint or steps down into the dictionary.
        """
        if isinstance(data, str):
            # We have a direct mounting like "api": "users"
            if namespace != "":
                # We are at the root level
                name = bp_name
            else:
                # We are inside a dictionary
                name = data

            # Create a new blueprint for the mount path
            bp = Blueprint(name, __name__)

            # Iterate through all files in the routes directory for this
            # path
            for file in glob.glob(f"backend/routes/{namespace}{data}/*.py"):
                # Convert paths like a/b/c to a.b.c as they are Python modules
                imp = file[:-3].replace("/", ".")

                # Import a the module to the variable
                module = importlib.import_module(imp)

                # Iterate through all members of the class
                for _, member in inspect.getmembers(module):
                    if (
                        inspect.isclass(member)  # Member is a class
                        and Route in member.__mro__  # derives from Route
                        and member is not Route  # it is not the route class
                    ):  # noqa
                        member.setup(bp)  # call the setup method of the route

            # Register the blueprint we created at the provided mount path
            self.app.register_blueprint(
                bp,
                url_prefix="/" + bp_name.replace(".", "/")
            )
        else:
            # If we are in a dictionary we need to iterate through all the
            # items but have a namespace set so we mount in the namespace
            for key, val in data.items():
                self.load_from_key_or_recurse(
                    f"{namespace}{bp_name}/",
                    f"{bp_name}/{key.replace('/', '')}",
                    val
                )

    def load_routes(self: "RouteManager") -> None:
        """Load the routes from the route directories."""
        # For every entry in the mappings
        for bp_name, path in MAPPINGS.items():
            # Load the entry
            self.load_from_key_or_recurse("", bp_name, path)
