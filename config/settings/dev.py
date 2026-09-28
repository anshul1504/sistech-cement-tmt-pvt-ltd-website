from .base import *  # noqa
from .base import env, BASE_DIR
import os

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = ["*"]

os.makedirs(BASE_DIR / "logs", exist_ok=True)

# Manifest static storage requires collectstatic; use plain storage in dev/test
# so `manage.py runserver`/`test` work without a build step.
STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}  # noqa: F405
