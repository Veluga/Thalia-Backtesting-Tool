from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from .extensions import db
from .forms import LoginForm, RegistrationForm
from .models.user import User

server_bp = Blueprint("main", __name__)


@server_bp.route("/")
def index():
    return render_template("index.html", title="Home Page")


@server_bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        error = validate_credentials(user, form.password.data)
        if error:
            return render_template("login.html", form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = find_next(backup="main.index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


def find_next(backup):
    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for(backup)
    return next_page


def validate_credentials(user, password):
    error = None
    if user is None:
        error = "Username not recognised"
    elif not user.check_password(password):
        error = "Incorrect password"
    return error


@server_bp.route("/logout/")
@login_required
def logout():
    logout_user()

    return redirect(url_for("main.index"))


@server_bp.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        if existing_username(form.username.data):
            error = "already registered"
            return render_template("register.html", form=form, error=error)
        else:
            save_user(form.username.data, form.password.data)
            return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)


def save_user(username, password):
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()


def existing_username(username):
    return User.query.filter_by(username=username).first()
