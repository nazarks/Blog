from flask import Blueprint, render_template

from blog.models.author import Author

author_app = Blueprint("author_app", __name__, url_prefix="/authors", static_folder="../static")


@author_app.route("/", endpoint="list")
def authors_list():
    authors = Author.query.all()
    return render_template("author/list.html", authors=authors)
