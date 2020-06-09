"""Edit the attributes of a class."""

from flask import Response, abort, g, redirect, render_template, request, url_for

from backend.models import Class, UserType
from backend.route import Route
from backend.utils import authenticated


class ClassEdit(Route):
    """A route for editing a class."""

    name = "edit"
    path = "/<int:class_id>/edit"

    @authenticated(user_type=UserType.TEACHER)
    def get(self, class_id: int) -> Response:
        """Return the view for editing a class."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        return render_template("teacher/class/edit.html", cls=cls)

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int) -> Response:
        """Edit a class."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        updatable_parameters = ["name"]

        for parameter in updatable_parameters:
            if param := request.form.get(parameter):
                setattr(cls, parameter, param)

        self.sess.commit()

        return redirect(url_for("teacher/class.details", class_id=class_id))
