"""A portal for allowing students to see their classes."""

from flask import Response, g, redirect, render_template, request, url_for

from backend.models import Class, ClassMembership, UserType
from backend.route import Route
from backend.utils import authenticated


class StudentJoin(Route):
    """A route for allowing a student to join a class."""

    name = "join"
    path = "/join"

    @authenticated(user_type=UserType.STUDENT)
    def post(self) -> Response:
        """Display a portal page to the user."""
        code = request.form.get("class_code")

        cls = Class.query.filter_by(code=code).first()

        if not cls:
            return render_template("student/index.html", error="Could not find class")

        class_membership = ClassMembership(user=g.user, cls=cls)

        self.app.db.session.add(class_membership)
        self.app.db.session.commit()
        return redirect(url_for("student.index"))
