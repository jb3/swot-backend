"""Route to manage the creation of users."""

import httpx
import parse
from flask import jsonify, render_template, request, Response
from sqlalchemy.exc import IntegrityError

from backend.config import CONFIG
from backend.database import Session
from backend.models import User
from backend.route import Route


class UserCreate(Route):
    """Create a new user."""

    name = "create"
    path = "/create"

    @staticmethod
    def get() -> Response:
        """Render a template to display a form to create users."""
        return render_template("users/create.html")

    @staticmethod
    def post() -> Response:
        """Use post data to create a new user."""
        # Validations
        required_fields = [
            "email",
            "password",
            "type",
            "full_name",
            "g-recaptcha",
        ]

        for key in required_fields:
            # If the key is missing, return HTTP 400 Bad Request
            if not request.form.get(key) or request.form.get(key).isspace():
                return (
                    jsonify({"status": "error", "field": [key, "missing"]}),
                    400,
                )

        if request.form["type"] not in ["student", "teacher", "parent"]:
            # If the passed type is not of one in the above list, raise 400
            return (
                jsonify({"status": "error", "field": ["type", "invalid"]}),
                400,
            )

        # Get a copy of the result
        data = request.form.copy()

        # Remove and save the google recaptcha score
        g_recaptcha = data.pop("g-recaptcha")

        recaptcha_response = httpx.post(
            # Request to Google to get the recaptcha score for the request
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                # Secret site key for recaptcha
                "secret": CONFIG.recaptcha.key,
                # Response from recaptcha to the client
                "response": g_recaptcha,
                # IP of the connecting user
                "remoteip": request.remote_addr,
            }
        ).json()

        if not recaptcha_response["success"]:
            # Recaptcha returned us an error and cannot evaluate the request
            return (
                jsonify(
                    {"status": "error", "field": ["recaptcha", "timeout"]}
                ),
                400,
            )

        if recaptcha_response["score"] < 0.5:
            # Scores under 0.5 are likely automated and should be blocked
            return (
                jsonify({"status": "error", "field": ["recaptcha", "failed"]}),
                400,
            )

        if data.pop("password_confirm") != data["password"]:
            return (
                jsonify({"status": "error", "field": ["password", "does not match"]}),
                400,
            )

        data["username"] = data["full_name"].lower().replace(" ", "_")

        # Create a new user with the provided data
        new_user = User(**data)

        # Create a new session with the database
        sess = Session()

        # Add the new user to the database
        sess.add(new_user)

        try:
            # Commit the new user to the database
            sess.commit()
        except IntegrityError as e:
            # An IntegrityError was raised, which means there was an issue
            # with a constraint on the database (i.e. username, email)
            if "duplicate key value" in e.orig.args[0]:
                # Parse the error to find the offending field
                field = parse.search(
                    'duplicate key value violates unique constraint "{}"',
                    e.orig.args[0],
                )
                # Return an error telling the client what was wrong
                return (
                    jsonify(
                        {"status": "error", "field": [field[0], "not_unique"]}
                    ),
                    400,
                )

        # If no errors were raised then the user creation succeeded
        return jsonify({"status": "success"})
