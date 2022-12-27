from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.models.user import User

user_app = Blueprint("user_app", __name__, url_prefix="/users", static_folder="../static")


@user_app.route("/", endpoint="list")
@login_required
def user_list():
    users = User.query.all()
    return render_template(
        "user/list.html",
        users=users,
    )


@user_app.route("/<int:pk>", endpoint="profile")
@user_app.route("/<int:pk>", endpoint="detail")
@login_required
def user_detail(pk: int):

    user = User.query.filter_by(id=pk).one_or_none()

    if user is None:
        raise NotFound(f"User id {pk} doesn't exists!")
    return render_template(
        "user/detail.html",
        user=user,
    )
