"""Delete a class and all associated information."""

from flask import abort, g, redirect, Response, url_for

from backend.route import Route
from backend.models import Class
from backend.utils import authenticated


class ClassInformation(Route):
    """A route for deleting a class."""

    name = "delete"
    path = "/delete/<int:class_id>"

    @authenticated(user_type="teacher")
    def post(self, class_id) -> Response:
        """Delete a class."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        self.sess.delete(cls)
        self.sess.commit()

        return redirect(url_for("teacher/.index"))
