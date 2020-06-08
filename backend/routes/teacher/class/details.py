"""Provide specifics on a class to a teacher."""

from flask import (
    abort,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    Response,
    url_for,
)

from backend.route import Route
from backend.models import Class, ClassMembership
from backend.utils import authenticated


class ClassInformation(Route):
    """A route for displaying classes."""

    name = "details"
    path = "/<int:class_id>"

    @authenticated(user_type="teacher")
    def get(self, class_id) -> Response:
        """Display a portal page to the user."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template("teacher/class/details.html", cls=cls)

    @authenticated(user_type="teacher")
    def delete(self, class_id) -> Response:
        """Remove a user from a class."""
        membership = (
            self.sess.query(ClassMembership)
            .filter_by(class_id=class_id, user_id=request.get_json().get("user_id"))
            .first()
        )

        if not membership:
            return abort(400)

        self.sess.delete(membership)
        self.sess.commit()

        return "OK", 200
