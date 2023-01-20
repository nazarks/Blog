from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from blog.forms.user import LoginForm, RegistrationForm
from blog.models import User
from blog.models.database import db

auth_app = Blueprint("auth_app", __name__, url_prefix="/auth", static_folder="../static")

login_manager = LoginManager()
login_manager.login_view = "auth_app.login"


@login_manager.user_loader
def load_user(pk):
    return User.query.filter_by(id=pk).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


@auth_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("general_app.index"))

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
            password=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("general_app.index"))

    return render_template("auth/register.html", form=form, error=error)


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():

    if current_user.is_authenticated:
        return redirect(url_for("general_app.index"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            return render_template("auth/login.html", form=form, error="Invalid email or password")

        login_user(user)
        return redirect(url_for("general_app.index"))

    return render_template("auth/login.html", form=form)


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("general_app.index"))


@auth_app.route("/secret/")
@login_required
def secret_views():
    return "super secret data"


__all__ = [
    "login_manager",
    "auth_app",
]
