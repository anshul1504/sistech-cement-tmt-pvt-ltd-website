"""
Base Django settings for the SISTECH Cement & TMT corporate site.
Split into base/dev/prod. Secrets come from .env via django-environ.
"""
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="django-insecure-change-me-in-env")

ADMIN_URL_PATH = env("ADMIN_URL_PATH", default="admin/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "jazzmin",
    "adminsortable2",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_ckeditor_5",
    "apps.core",
    "apps.products",
    "apps.network",
    "apps.programs",
    "apps.company",
    "apps.media_center",
    "apps.careers",
    "apps.faq",
    "apps.enquiries",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_and_theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Career resumes go in a non-listable subfolder, served only via a controlled view.
RESUME_UPLOAD_SUBDIR = "resumes"
RESUME_MAX_SIZE_MB = env.int("RESUME_MAX_SIZE_MB", default=5)
RESUME_ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]

# Whether the CSS build command output should be preferred over source files.
USE_BUILT_CSS = env.bool("USE_BUILT_CSS", default=False)

# --- Email ---
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@sistechcement.example")

# --- CKEditor 5 ---
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|", "bold", "italic", "link", "bulletedList",
            "numberedList", "blockQuote", "|", "undo", "redo", "|", "sourceEditing",
        ],
    },
}
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# --- Rate limiting for form spam protection ---
FORM_RATE_LIMIT_SECONDS = env.int("FORM_RATE_LIMIT_SECONDS", default=60)

LOGIN_URL = f"/{ADMIN_URL_PATH}login/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[{asctime}] {levelname} {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "sistech.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

JAZZMIN_SETTINGS = {
    "site_title": "SISTECH Admin",
    "site_header": "SISTECH",
    "site_brand": "SISTECH Cement & TMT",
    "welcome_sign": "Welcome to the SISTECH website admin",
    "copyright": "SISTECH Cement & TMT Pvt. Ltd.",
    "site_icon": "favicon.ico",
    "show_ui_builder": False,
    "related_modal_active": True,
    "topmenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.SiteSettings": "fas fa-cogs",
        "core.ThemeSettings": "fas fa-palette",
        "core.Page": "fas fa-file-alt",
        "core.MenuItem": "fas fa-bars",
        "core.HeroSlide": "fas fa-images",
        "enquiries.ContactEnquiry": "fas fa-envelope",
        "network.DealerApplication": "fas fa-handshake",
        "careers.JobApplication": "fas fa-user-tie",
        "media_center.BlogPost": "fas fa-newspaper",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "brand_colour": "navbar-primary",
    "accent": "accent-warning",
    "sidebar": "sidebar-dark-primary",
    "sidebar_fixed": True,
    "sidebar_nav_child_indent": True,
    "theme": "flatly",
}
