import os

from .base import *  # noqa
from .base import env, BASE_DIR

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

os.makedirs(BASE_DIR / "logs", exist_ok=True)

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# Minimal CSP: self by default, allow inline style block for theme vars and GA if configured.
SECURE_REFERRER_POLICY = "same-origin"

USE_BUILT_CSS = True
