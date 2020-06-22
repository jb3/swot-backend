"""Test the user creation route."""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import pytest
from flask import testing

from app import manager
from backend.routes.users.sign_up import UserSignUp
from backend.models import UserType


@pytest.fixture(scope="module")
def client() -> testing.FlaskClient:
    """Create a client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def authorized_client() -> testing.FlaskClient:
    """Create a logged in client for querying flask to emulate a HTTP client."""
    with manager.app.test_client() as client:
        with client.session_transaction() as session:
            session["uid"] = 123
        yield client


def test_sign_up_get(client: testing.FlaskClient) -> None:
    """Test the route to render the user sign up page."""
    resp = client.get("/users/sign_up")
    assert "Sign up • Swot".encode() in resp.data


def test_signed_in_user(authorized_client: testing.FlaskClient) -> None:
    """Test that a signed in user trying to access the page is redirected."""
    print(authorized_client.get("/users/sign_up"))
    assert authorized_client.get("/users/sign_up").status_code == 302


def test_validations() -> None:
    """Test validations on form data."""
    assert (
        list(
            UserSignUp._validate_required(
                {
                    "email": "test@example.com",
                    "password": "abcdef",
                    "password_confirm": "abcdef",
                    "type": "teacher",
                    "full_name": "Test User",
                    "g-recaptcha": "aabbccdd",
                }
            )
        )
        == []
    )

    assert list(
        UserSignUp._validate_required(
            {
                "password": "abcdef",
                "password_confirm": "abcdef",
                "type": "teacher",
                "full_name": "Test User",
                "g-recaptcha": "aabbccdd",
            }
        )
    ) == ["email"]


def test_type_parse() -> None:
    """Test the parsing of types into enumerables."""
    assert UserSignUp._parse_type("teacher") is UserType.TEACHER
    assert UserSignUp._parse_type("student") is UserType.STUDENT
    assert UserSignUp._parse_type("parent") is UserType.PARENT


def test_unique_constraint_parser() -> None:
    """Test the parser for unique violations."""
    assert (
        UserSignUp._get_unique_failure(
            'duplicate key value violates unique constraint "users_test_field_key"'
        )
        == "test_field"
    )


def test_password_hasher() -> None:
    """Test password hash utility."""
    hashed = UserSignUp._hash_password("testing")

    hasher = PasswordHasher()

    assert hasher.verify(hashed, "testing")

    with pytest.raises(VerifyMismatchError):
        hasher.verify(hashed, "not testing")
