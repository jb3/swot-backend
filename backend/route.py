from flask import Blueprint
from flask.views import MethodView


class Route(MethodView):
    """Base class for the routes."""

    name = None
    blueprint = None
    path = None

    @classmethod
    def setup(cls: "Route", manager: "backend.route_manager.RouteManager", blueprint: Blueprint):
        """Setup the view with the blueprint."""
        print(cls.name)
        if not cls.path or not cls.name:
            raise RuntimeError("Routes have name and path defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))

        cls.blueprint = blueprint.name
        cls.name = f"{blueprint.name}.{cls.name}"
