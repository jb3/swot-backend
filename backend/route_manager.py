"""Manage routes for application."""
import importlib
import inspect
from pathlib import Path

from flask import Blueprint, Flask, Response, session
from flask_wtf.csrf import CSRFProtect

from .config import CONFIG
from .models import db, User
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
        self.app.config.update(**dict(CONFIG.flask))

        # Register the after_request hook with flask to run a function
        # after every request
        self.app.after_request(self.after_request)

        # Protect the application from Cross-Site Request Forgery
        CSRFProtect(self.app)

        url = "postgresql://{}:{}@{}:{}/{}"
        url = url.format(
            CONFIG.db.username,
            CONFIG.db.password,
            CONFIG.db.host,
            CONFIG.db.port,
            CONFIG.db.database,
        )

        self.app.config["SQLALCHEMY_DATABASE_URI"] = url

        db.init_app(self.app)

        self.app.db = db

        # Load all the routes
        self.load_routes()

        self.app.context_processor(self.inject_user())

    def run(self: "RouteManager") -> None:
        """Start the flask application."""
        # Start the web application on the parameters provided in YAML
        self.app.run(
            host=CONFIG.host.host, port=CONFIG.host.port, debug=CONFIG.host.debug,
        )

    @staticmethod
    def after_request(response: Response) -> Response:
        """Process a response before it is sent to the client."""
        return response

    @staticmethod
    def inject_user() -> dict:
        """Inject a user variable into all templates."""

        def inject() -> dict:
            user = None

            if session.get("uid"):
                uid = session.get("uid")
                user = User.query.filter_by(id=uid).first()

            return dict(user=user)

        return inject

    def load(self: "RouteManager") -> None:
        """
        Load a mapping file or recurse into a directory.

        The mapping file may specify an area as either a string for the route
        or a dictionary which should be recursed into. This function either
        loads the blueprint or steps down into the dictionary.
        """
        blueprints = {}

        used_classes = {}

        for path in Path("backend/routes").rglob("*.py"):
            file = str(path)
            # Convert paths like a/b/c to a.b.c as they are Python modules
            imp = file[:-3].replace("/", ".")
            bp_name = "/".join(imp.split(".")[::-1][1:][::-1][2:])

            if bp_name == "":
                bp_name = "index"

            if blueprints.get(bp_name):
                bp = blueprints.get(bp_name)
            else:
                bp = Blueprint(bp_name, imp)
                blueprints[bp_name] = bp

            # Import a the module to the variable
            module = importlib.import_module(imp)

            # Iterate through all members of the class
            for _, member in inspect.getmembers(module):
                if (
                    inspect.isclass(member)  # Member is a class
                    and Route in member.__mro__  # derives from Route
                    and member is not Route  # it is not the route class
                ):  # noqa
                    if member.__name__ in used_classes:
                        raise RuntimeError(
                            f"Two classes are using the name, '{member.__name__}' from"
                            f" {file} and {used_classes[member.__name__]}"
                        )
                    used_classes[member.__name__] = file
                    member.setup(bp, self.app)  # call the setup method of the route

        for path, bp in blueprints.items():
            if path == "index":
                path = ""

            self.app.register_blueprint(bp, url_prefix="/" + path)

    def load_routes(self: "RouteManager") -> None:
        """Load the routes from the route directories."""
        self.load()
