"""Base methods and functions for creating routes."""
from flask import Flask, Blueprint
from flask.views import MethodView



class Route(MethodView):
    """Base class for the routes."""

    name = None
    blueprint = None
    path = None

    sess = None

    @classmethod
    def setup(cls: "Route", blueprint: Blueprint, app: Flask) -> "Route":
        """Register the view with the blueprint."""
        if not cls.path or not cls.name:
            raise RuntimeError("Routes have name and path defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))

        cls.blueprint = blueprint.name
        cls.app = app

        return cls
