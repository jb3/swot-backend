"""Delete a class and all associated information."""

from flask import Response, abort, g, redirect, url_for

from backend.models import Class, UserType
from backend.route import Route
from backend.utils import authenticated


class ClassDelete(Route):
    """A route for deleting a class."""

    name = "delete"
    path = "/delete/<int:class_id>/edit"

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int) -> Response:
        """Delete a class."""
        cls = Class.query.filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        self.app.db.session.delete(cls)
        self.app.db.session.commit()

        return redirect(url_for("teacher.index"))
