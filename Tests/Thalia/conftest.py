import os
import tempfile

import pytest

from Thalia import create_app
from Thalia.extensions import db
from Thalia.models.user import User

NAME = "test_default"
PW = "test_mypw"


@pytest.fixture
def app():
    """
    replaces the Thalia.__init__-file for the tests
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "WTF_CSRF_ENABLED": False,  # I think necessary for testing forms
        }
    )
    ctx = app.app_context()  # makes current_app point to this app
    ctx.push()

    db.create_all()  # I think only inits the ORM stuff

    yield app

    ctx.pop()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def default_user():
    new_user = User(username=NAME)
    new_user.set_password(PW)
    db.session.add(new_user)
    db.session.commit()

    yield {"username": NAME, "password": PW}

    db.session.delete(new_user)


@pytest.fixture
def client(app):
    """
    Allows test to make requests to the application without running the server
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    # stolen from official docs
    def __init__(self, client):
        self._client = client

    def login(self, username=NAME, password=PW):
        return self._client.post(
            "/login",
            follow_redirects=True,
            data={"username": username, "password": password},
        )

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)
