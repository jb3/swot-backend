"""Route for signing into Swot."""
import httpx
from argon2 import PasswordHasher
from flask import redirect, render_template, request, Response, session, url_for

from backend.config import CONFIG
from backend.database import Session
from backend.models import User
from backend.route import Route


class UserSignIn(Route):
    """Route for signing into Swot."""

    name = "sign_in"
    path = "/sign_in"

    @staticmethod
    def get() -> Response:
        """GET request to the Page index."""
        # Render the user creation page
        if session.get("uid"):
            return redirect(url_for("pages.index"))

        return render_template("users/sign_in.html", errors={})

    @staticmethod
    def post() -> Response:
        """Use post data to login a user."""
        # Validations
        required_fields = [
            "email",
            "password",
            "g-recaptcha",
        ]

        errors = {}

        for key in required_fields:
            # If the key is missing, return HTTP 400 Bad Request
            if not request.form.get(key) or request.form.get(key).isspace():
                errors[key] = f"{key.replace('_', ' ').capitalize()} is not present"

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
            },
        ).json()

        if not recaptcha_response["success"]:
            # Recaptcha returned us an error and cannot evaluate the request
            # Set error in email since it is top field
            errors["email"] = "ReCAPTCHA did not complete"
        else:
            if recaptcha_response["score"] < 0.5:
                # Scores under 0.5 are likely automated and should be blocked
                errors["email"] = "ReCAPTCHA failed"

        hasher = PasswordHasher()

        # Create a new session with the database
        sess = Session()

        user = sess.query(User).filter_by(email=data["email"]).first()

        if user is None:
            errors["email"] = "Email or password incorrect"

        valid = hasher.verify(user.password, data["password"])

        if not valid:
            errors["email"] = "Email or password incorrect"

        # If no errors were raised then the user creation succeeded
        if len(errors) == 0:
            session["uid"] = user.id
            return redirect(url_for("users.user"))

        return render_template("users/sign_in.html", errors=errors), 400
