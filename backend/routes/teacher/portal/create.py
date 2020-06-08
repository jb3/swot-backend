"""A portal for allowing teachers to create a new classe."""

from flask import g, redirect, render_template, request, Response, url_for

from backend.models import Class
from backend.route import Route
from backend.utils import authenticated, code_generate


class CreateClass(Route):
    """A route for displaying classes."""

    name = "create"
    path = "/create"

    @authenticated(user_type="teacher")
    def get(self) -> Response:  # skipcq: PYL-R0201
        """Display form to the user."""
        return render_template("teacher/create.html")

    @authenticated(user_type="teacher")
    def post(self) -> Response:
        """Create a new class with provided data."""
        # Confirm a name was passed
        if request.form.get("name") is None:
            return render_template(
                "teacher/create.html", error="You need to provide a name for your class"
            )

        # Confirm the name is not just spaces
        if request.form.get("name").isspace() or request.form.get("name") == "":
            return render_template(
                "teacher/create.html", error="You need to provide a name for your class"
            )

        # Assign the name from the form to a variable
        name = request.form.get("name")

        # Check the authenticated user does not have a class of the same name
        exists = (
            self.sess.query(Class).filter_by(owner_id=g.user.id, name=name).first()
            is not None
        )

        # Return an error if they do
        if exists:
            return render_template(
                "teacher/create.html", error="You already have a class of this name"
            )

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

        cls = Class(name=name, code=code, owner_id=g.user.id)

        # Add the new class
        self.sess.add(cls)

        # Commit changes
        self.sess.commit()

        return redirect(url_for("teacher/.index"))
