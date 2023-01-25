import os

from dotenv import load_dotenv

from blog.enums import EnvType

# set environment here
CONFIG_NAME = EnvType.development_local.name

load_dotenv(f"{CONFIG_NAME}.env")

ENV = os.getenv("FLASK_ENV", default=EnvType.production)
DEBUG = os.getenv("FLASK_DEBUG")

SECRET_KEY = os.getenv("SECRET_KEY")
WTF_CSRF_ENABLED = True
FLASK_ADMIN_SWATCH = "cosmo"


if CONFIG_NAME == EnvType.development_local.name:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
else:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
