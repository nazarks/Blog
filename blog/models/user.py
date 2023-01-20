from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from blog.models.database import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)  # noqa: VNE003, A003
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, default="", server_default="")
    password = Column(String(255), nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")

    author = relationship("Author", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<User #{self.id} {self.username}>"
