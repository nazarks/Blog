from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from blog.forms.article import CreateArticleForm
from blog.models import Article, Author
from blog.models.database import db

article_app = Blueprint("article_app", __name__, url_prefix="/articles", static_folder="../static")


@article_app.route("/", endpoint="list")
def article_list():
    articles = Article.query.all()
    return render_template(
        "article/list.html",
        articles=articles,
    )


@article_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id):
    article = Article.query.filter_by(id=article_id).one_or_none()
    if not article:
        raise NotFound
    return render_template(
        "article/details.html",
        article=article,
    )


@article_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_artilce():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)
        db.session.add(article)
        if current_user.author:
            article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author_id = author.id

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create a new article!"
        else:
            return redirect(url_for("article_app.details", article_id=article.id))

    return render_template("article/create.html", form=form, error=error)
