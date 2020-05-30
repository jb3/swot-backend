"""Route for signing up for Swot."""
import httpx
import parse
from argon2 import PasswordHasher
from flask import redirect, render_template, request, Response, session, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import ImmutableMultiDict

from backend.config import CONFIG
from backend.database import Session
from backend.models import User
from backend.route import Route


class UserSignUp(Route):
    """Route for signing up for Swot."""

    name = "sign_up"
    path = "/sign_up"

    @staticmethod
    def get() -> Response:
        """GET request to the Page index."""
        # Render the user creation page
        if session.get("uid"):
            return redirect(url_for("pages.index"))

        return render_template("users/sign_up.html", errors={})

    @staticmethod
    def _validate_required(form: ImmutableMultiDict) -> list:
        """Validate that the required fields for user sign up are present."""
        required_fields = [
            "email",
            "password",
            "password_confirm",
            "type",
            "full_name",
            "g-recaptcha",
        ]

        for key in required_fields:
            # If the key is missing, return HTTP 400 Bad Request
            if not request.form.get(key) or request.form.get(key).isspace():
                yield key

    @staticmethod
    def _do_recaptcha(gr_resp: str) -> dict:
        """Make a request to recaptcha."""
        return httpx.post(
            # Request to Google to get the recaptcha score for the request
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                # Secret site key for recaptcha
                "secret": CONFIG.recaptcha.key,
                # Response from recaptcha to the client
                "response": gr_resp,
                # IP of the connecting user
                "remoteip": request.remote_addr,
            },
        ).json()

    @staticmethod
    def _get_unique_failure(arg: str) -> str:
        """Find the failing unique constraint."""
        constraint = parse.search(
            'duplicate key value violates unique constraint "{}"', arg,
        )

        # Constraints are in the format of users_X_key where X is the violating
        # unique constraint.
        field = parse.search("users_{}_key", constraint[0])

        return field[0]

    @staticmethod
    def _hash_password(passwd: str) -> str:
        """Hash a password with Argon2."""
        hasher = PasswordHasher()
        return hasher.hash(passwd)

    def post(self: "Route") -> Response:
        """Use post data to create a new user."""
        errors = {}

        for key in self._validate_required(request.form):
            errors[key] = f"{key.replace('_', ' ').capitalize()} is not present"

        if request.form.get("type") not in ["student", "teacher", "parent"]:
            # If the passed type is not of one in the above list, raise 400
            errors["type"] = "Invalid type"

        # Get a copy of the result
        data = request.form.copy()

        # Remove and save the google recaptcha score
        g_recaptcha = data.pop("g-recaptcha")

        recaptcha_response = self._do_recaptcha(g_recaptcha)

        if not recaptcha_response["success"]:
            # Recaptcha returned us an error and cannot evaluate the request
            # Set error in full_name since it is top field
            errors["full_name"] = "ReCAPTCHA did not complete"
        else:
            if recaptcha_response["score"] < 0.5:
                # Scores under 0.5 are likely automated and should be blocked
                errors["full_name"] = "ReCAPTCHA failed"

        if data.pop("password_confirm") != data["password"]:
            errors["password_confirm"] = "Does not match password"

        data["password"] = self._hash_password(data["password"])

        data["username"] = data["full_name"].lower().replace(" ", "_")

        # Create a new session with the database
        sess = Session()

        user = sess.query(User).filter_by(username=data["username"])
        acc = 0

        if user is not None:
            while True:
                acc += 1

                user = (
                    sess.query(User)
                    .filter_by(username=data["username"] + str(acc))
                    .first()
                )

                if user is None:
                    data["username"] += str(acc)
                    break

        data.pop("_csrf_token")

        # Create a new user with the provided data
        new_user = User(**data)

        try:
            # Commit the new user to the database if no errors have occurred
            if len(errors) == 0:
                # Add the new user to the database
                sess.add(new_user)

                sess.commit()

                sess.refresh(new_user)
        except IntegrityError as e:
            # An IntegrityError was raised, which means there was an issue
            # with a constraint on the database (i.e. username, email)
            if "duplicate key value" in e.orig.args[0]:
                # Parse the error to find the offending field
                field = self._get_unique_failure(e.orig.args[0])

                errors[field] = f"{field.replace('_', ' ').capitalize()} already in use"

        # If no errors were raised then the user creation succeeded
        if len(errors) == 0:
            session["uid"] = new_user.id
            return redirect(url_for("pages.index"))

        return render_template("users/sign_up.html", errors=errors), 400
