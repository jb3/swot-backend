"""A portal for allowing students to see their classes."""

from flask import g, redirect, render_template, request, Response, url_for

from backend.route import Route
from backend.utils import authenticated
from backend.models import Class, ClassMembership


class StudentJoin(Route):
    """A route for allowing a student to join a class."""

    name = "join"
    path = "/join"

    @authenticated(user_type="student")
    def post(self) -> Response:
        """Display a portal page to the user."""
        code = request.form.get("class_code")

        cls = self.sess.query(Class).filter_by(code=code).first()

        if not cls:
            return render_template("student/index.html", error="Could not find class")

        class_membership = ClassMembership(user=g.user, cls=cls)

        self.sess.add(class_membership)
        self.sess.commit()
        return redirect(url_for("student.index"))
