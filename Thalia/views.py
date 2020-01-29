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
        if user is None:
            error = "Username not recognised"
            return render_template("login.html", form=form, error=error)
        elif not user.check_password(form.password.data):
            error = "Incorrect password"
            return render_template("login.html", form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


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
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            error = "already registered"
            return render_template("register.html", form=form, error=error)

        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html", title="Register", form=form)
