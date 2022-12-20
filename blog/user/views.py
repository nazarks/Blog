from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

user_app = Blueprint("user_app", __name__, url_prefix="/users", static_folder="../static")

USERS = {
    1: "John",
    2: "Nik",
    3: "Kate",
}


@user_app.route("/", endpoint="list")
def user_list():
    return render_template(
        "user/list.html",
        users=USERS,
    )


@user_app.route("/<int:pk>", endpoint="detail")
def user_detail(pk):
    try:
        user_name = USERS[pk]
    except KeyError:
        raise NotFound(f"User id {pk} doesn't exists!")
    return render_template(
        "user/detail.html",
        user_name=user_name,
    )
