from flask import Flask

from blog.article.views import article_app
from blog.general.views import general_app
from blog.user.views import user_app


def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    return app


def register_blueprint(app):
    app.register_blueprint(general_app)
    app.register_blueprint(user_app)
    app.register_blueprint(article_app)
