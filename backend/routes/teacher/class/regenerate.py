"""Regenerate the join code for a class."""

from flask import Response, abort, g, redirect, url_for

from backend.models import Class, UserType
from backend.route import Route
from backend.utils import authenticated, code_generate


class ClassRegenerate(Route):
    """A route for regenerating the join code for a class."""

    name = "regenerate"
    path = "/<int:class_id>/regenerate"

    @authenticated(user_type=UserType.TEACHER)
    def post(self, class_id: int) -> Response:
        """Regenerate a class code."""
        cls = self.sess.query(Class).filter_by(id=class_id).first()

        if not cls:
            return abort(404)

        if cls.owner.id != g.user.id:
            return abort(403)

        while True:
            # Generate a code
            code = code_generate(k=6)
            # Check it doesn't exist
            code_exists = (
                self.sess.query(Class).filter_by(code=code).first() is not None
            )

            # If it doesn't stop generating codes
            if not code_exists:
                break

        cls.code = code
        self.sess.commit()

        return redirect(url_for("teacher/class.details", class_id=class_id))
