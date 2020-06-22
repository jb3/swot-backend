"""Utilities for working with the web application."""

import random
import string
from functools import wraps
from typing import Callable

from flask import abort, g, redirect, session, url_for

from backend.models import User


def authenticated(user_type: str = "any") -> Callable:
    """
    Decorate a route to ensure access is by an authenticated user.

    This decorator works by fetching the uid from the session and verifying it is an
    existing user, it also attaches it to the request for usage in route processing.

    The logged in user is stored in g.user, where g is the Flask application context
    global session.
    """

    def wrap(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):  # noqa
            uid = session.get("uid")
            if uid:
                user = User.query.filter_by(id=uid).first()
                g.user = user

                if user:
                    if user_type != "any":
                        if user.type is not user_type:
                            # We are looking for a different type of user, return HTTP
                            # 403 which is the error code for unauthorized access.
                            return abort(403)

                    return func(self, *args, **kwargs)

            return redirect(url_for("users.sign_in"))

        return wrapper

    return wrap


def code_generate(k: int) -> str:
    """Generate a code for a class."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=k))
