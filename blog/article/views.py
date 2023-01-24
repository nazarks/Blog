from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.forms.article import CreateArticleForm
from blog.models import Article, Author, Tag
from blog.models.database import db

article_app = Blueprint("article_app", __name__, url_prefix="/articles", static_folder="../static")


@article_app.route("/", endpoint="list")
def article_list():
    articles = Article.query.all()
    return render_template(
        "article/list.html",
        articles=articles,
    )


@article_app.route("/tag/<int:tag_id>", endpoint="list_by_tag")
def article_list_by_tag(tag_id):
    articles = db.session.query(Article)
    articles = articles.filter(Article.tags.any(Tag.id == tag_id))
    tag = Tag.query.filter_by(id=tag_id).first()
    return render_template(
        "article/list_by_tag.html",
        articles=articles,
        tag=tag,
    )


@article_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id):
    article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()
    if not article:
        raise NotFound
    return render_template(
        "article/details.html",
        article=article,
    )


@article_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)

    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]

    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)

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
