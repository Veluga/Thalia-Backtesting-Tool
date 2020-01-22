"""App config."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'app.dbexport')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # secret key used to fight agains CSRF attacks: http://en.wikipedia.org/wiki/Cross-site_request_forgery
    SECRET_KEY = os.environ.get("SECRET_KEY", "d9eb813bafdb11441f398e0b3f350066")
