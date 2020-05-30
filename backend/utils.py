"""Utilities for working with the web application."""

from functools import wraps
from typing import Callable

from flask import g, redirect, session, url_for

from backend.database import Session
from backend.models import User


def authenticated(func: Callable) -> Callable:
    """
    Decorate a route to ensure access is by an authenticated user.

    This decorator works by fetching the uid from the session and verifying it is an
    existing user, it also attaches it to the request for usage in route processing.

    The logged in user is stored in g.user, where g is the Flask application context
    global session.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):  # noqa
        uid = session.get("uid")
        if uid:
            sess = Session()
            user = sess.query(User).filter_by(id=uid).first()

            if user:
                g.user = user
                return func(*args, **kwargs)

        return redirect(url_for("users.sign_in"))

    return wrapper
