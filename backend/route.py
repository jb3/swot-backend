"""Base methods and functions for creating routes."""
from flask import Blueprint
from flask.views import MethodView

from backend.database import Session


class Route(MethodView):
    """Base class for the routes."""

    name = None
    blueprint = None
    path = None

    sess = None

    @classmethod
    def setup(cls: "Route", blueprint: Blueprint, db_session: Session) -> "Route":
        """Register the view with the blueprint."""
        if not cls.path or not cls.name:
            raise RuntimeError("Routes have name and path defined")

        blueprint.add_url_rule(cls.path, view_func=cls.as_view(cls.name))

        cls.blueprint = blueprint.name

        cls.sess = db_session

        return cls
