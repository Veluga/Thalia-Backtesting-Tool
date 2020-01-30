import pytest
from flask import session
from flask_login import current_user

from Thalia.models.user import User


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/register", follow_redirects=True).status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        "/register", data={"username": "a", "password": "a"}, follow_redirects=True
    )
    # TODO: more long term test for checking page
    assert b"Sign In" in response.data

    # test that the user was inserted into the database
    with app.app_context():
        assert User.query.filter_by(username="a").first() is not None


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Username not recognised"), ("test", "a", b"Incorrect password")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):

    with client:
        auth.login()
        assert "user_id" in session, "login needs to work"
        auth.logout()
        assert "user_id" not in session, "user_id should be forgotten on logout"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        # TODO: test missing username or pw
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/register",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    assert message in response.data


def test_login(app, client, auth):
    # test that viewing the page renders without template errors
    assert client.get("/login", follow_redirects=True).status_code == 200

    # test that successful login redirects to the index page
    response = auth.login()

    # this is a poor way to test if redirected to homepage while logged in
    # ideally it would test if path is "/" and or something more
    assert b"Hi, test" in response.data

    # login request set the user_id in the session
    # check that the user is loaded from the session
    # TODO: find purpose of this test
    with client:
        client.get("/")
        assert session["user_id"] == "1"
        assert current_user.username == "test"

    # test redirection of login page to home when already signed in
    response = client.get("/login", follow_redirects=True)
    assert b"Hi, test" in response.data

    # test redirection of registration page to home when already signed in
    response = client.get("/register", follow_redirects=True)
    assert b"Hi, test" in response.data

# TODO: if trying to access /dashboard while logged out, redirect to login page
