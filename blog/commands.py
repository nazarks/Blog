import click
from werkzeug.security import generate_password_hash

from blog.models.database import db


@click.command("init-db")
def init_db():
    """
    Run in your terminal:
    flask init-db
    """
    db.create_all()
    print("done!")


@click.command("create-init-users")
def create_init_users():
    """
    Run in your terminal:
    flask create-init-users
    """
    from blog.models import User

    users = [
        User(username="Admin", is_staff=True, email="admin@site.com", password=generate_password_hash("test123")),
        User(username="James", email="james@site.com", password=generate_password_hash("test123")),
        User(username="Nik", email="nik@site.com", password=generate_password_hash("test123")),
    ]

    db.session.add_all(users)
    db.session.commit()
    print(f"done! created users: { [user.username for user in users]}")


@click.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    flask create-tags
    """
    from blog.models import Tag

    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()

    print("created tags")
