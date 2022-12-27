from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from blog.models import User

auth_app = Blueprint("auth_app", __name__, url_prefix="/auth", static_folder="../static")

login_manager = LoginManager()
login_manager.login_view = "auth_app.login"


@login_manager.user_loader
def load_user(pk):
    return User.query.filter_by(id=pk).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "GET" and not current_user.is_authenticated:
        return render_template("auth/login.html")

    if request.method == "GET" and current_user.is_authenticated:
        return redirect(url_for("general_app.index"))

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Check your login details")
        return redirect(url_for(".login"))

    login_user(user)

    return redirect(url_for("general_app.index"))


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
