from flask import Blueprint, render_template

general_app = Blueprint("general_app", __name__, static_folder="../static")


@general_app.route("/", endpoint="index")
def index():
    return render_template("general/index.html")
