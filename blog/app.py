from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from blog import commands
from blog.admin import admin
from blog.api import init_api
from blog.article.views import article_app
from blog.auth.views import auth_app, login_manager
from blog.author.view import author_app
from blog.general.views import general_app
from blog.models.database import db
from blog.user.views import user_app


def create_app():
    app = Flask(__name__)
    app.config.from_object("blog.config")

    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    return app


def register_blueprint(app):
    app.register_blueprint(general_app)
    app.register_blueprint(user_app)
    app.register_blueprint(article_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(author_app)


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, compare_type=True)

    # Disabled for API test
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    login_manager.init_app(app)

    admin.init_app(app)

    api = init_api(app)


def register_commands(app):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_init_users)
    app.cli.add_command(commands.create_tags)
