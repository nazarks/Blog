from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from blog.user.views import USERS

article_app = Blueprint("article_app", __name__, url_prefix="/articles", static_folder="../static")


ARTICLES = {
    1: {
        "title": "Django",
        "text": "Django Article Text",
        "author": 1,
    },
    2: {
        "title": "Flask",
        "text": "Flask Article Text",
        "author": 2,
    },
    3: {
        "title": "FastAPI",
        "text": "FastAPI Article Text",
        "author": 3,
    },
}


@article_app.route("/", endpoint="list")
def article_list():
    return render_template(
        "article/list.html",
        articles=ARTICLES,
    )


@article_app.route("/<int:pk>", endpoint="detail")
def article_detail(pk):
    try:
        article = ARTICLES[pk]
    except KeyError:
        raise NotFound(f"Article id {pk} doesn't exists!")
    user_name = USERS[article["author"]]
    return render_template(
        "article/detail.html",
        article=article,
        user_name=user_name,
    )
