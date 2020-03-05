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

    def get(self: "UserCreate") -> Response:
        """Render a template to display a form to create users."""
        return render_template("users/create.html")

    def post(self: "UserCreate") -> Response:
        """Use post data to create a new user."""
        # Validations
        required_fields = [
            "email",
            "password",
            "type",
            "username",
            "full_name",
            "g-recaptcha",
        ]

        for key in required_fields:
            if not request.form.get(key) or request.form.get(key).isspace():
                return (
                    jsonify({"status": "error", "field": [key, "missing"]}),
                    400,
                )

        if request.form["type"] not in ["student", "teacher", "parent"]:
            return (
                jsonify({"status": "error", "field": ["type", "invalid"]}),
                400,
            )

        data = request.form.copy()
        g_recaptcha = data.pop("g-recaptcha")

        # NOTE: This must specify a local certificate because of
        # the self signed certificate used by the web filter at Malton School.
        recaptcha_response = httpx.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": CONFIG.recaptcha.key,
                "response": g_recaptcha,
                "remoteip": request.remote_addr,
            },
            verify="Malton School HTTPS.pem",
        ).json()

        if not recaptcha_response["success"]:
            return (
                jsonify(
                    {"status": "error", "field": ["recaptcha", "timeout"]}
                ),
                400,
            )

        if recaptcha_response["score"] < 0.5:
            return (
                jsonify({"status": "error", "field": ["recaptcha", "failed"]}),
                400,
            )

        new_user = User(**data)

        sess = Session()

        sess.add(new_user)

        try:
            sess.commit()
        except IntegrityError as e:
            if "duplicate key value" in e.orig.args[0]:
                field = parse.search(
                    'duplicate key value violates unique constraint "{}"',
                    e.orig.args[0],
                )
                return (
                    jsonify(
                        {"status": "error", "field": [field[0], "not_unique"]}
                    ),
                    400,
                )

        return jsonify({"status": "success"})
