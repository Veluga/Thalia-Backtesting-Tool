from Thalia.extensions import db
from Thalia.models import user


def test_new_user(client):
    """
    functional test for testing user creation and storage
    """
    name = "john smith"
    pw = "123456"
    new_user = user.User(username=name)
    new_user.set_password(pw)

    assert new_user.password_hash != pw, "passwords should be hashed"
    assert new_user.check_password(pw), "checking the same pw should return true"

    db.session.add(new_user)
    db.session.commit()

    id_ = user.User.query.filter_by(username=name).first().id
    same_user = user.load_user(id_)
    assert same_user == new_user, "user should be accessible from database"
