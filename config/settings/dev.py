"""Dev configuration."""

import os
from pathlib import Path

from .base import *  # noqa
from .base import env

DEBUG = True

SECRET_KEY = env.str("SECRET_KEY", "dev_secret_key")

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_HOSTS = [host for host in env.str("ALLOWED_HOSTS", "").split(",") if host]
ALLOWED_HOSTS = ENV_HOSTS + [
    "localhost",
    "127.0.0.1",
]

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
