"""Provide specifics on a class to a teacher."""

from flask import Response, abort, g, render_template, request

from backend.models import Class, ClassMembership, UserType
from backend.route import Route
from backend.utils import authenticated


class ClassInformation(Route):
    """A route for displaying classes."""

    name = "details"
    path = "/<int:class_id>"

    @authenticated(user_type=UserType.TEACHER)
    def get(self, class_id: int) -> Response:
        """Display a portal page to the user."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template("teacher/class/details.html", cls=cls)

    @authenticated(user_type=UserType.TEACHER)
    def delete(self, class_id: int) -> Response:
        """Remove a user from a class."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        membership = (
            ClassMembership
            .query
            .filter_by(class_id=class_id, user_id=request.get_json().get("user_id"))
            .first()
        )

        if not membership:
            return abort(400)

        self.app.db.session.delete(membership)
        self.app.db.session.commit()

        return "OK", 200
