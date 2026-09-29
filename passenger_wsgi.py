"""Entry point for cPanel "Setup Python App" (Passenger). Uses production settings."""
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.prod"

from config.wsgi import application  # noqa: E402
