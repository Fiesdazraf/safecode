"""
Django settings for mysite project (SafeCode Portfolio).
Ready for local development and deployment (PythonAnywhere / Koyeb).
"""

from pathlib import Path
import os
from urllib.parse import urlparse

# ------------------------------------------------------------------------------
# Base & environment
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env in local dev
from dotenv import load_dotenv  # comment: load environment variables if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)

# ------------------------------------------------------------------------------
# Security & core
# ------------------------------------------------------------------------------

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-key-for-dev-only")

# Default DEBUG=True for local, set DJANGO_DEBUG=False on servers
DEBUG = os.getenv("DJANGO_DEBUG", "True").strip().lower() == "true"

# Allowed hosts
_default_hosts = "localhost,127.0.0.1,farzadseif.pythonanywhere.com"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("DJANGO_ALLOWED_HOSTS", _default_hosts).split(",")
    if h.strip()
]

# CSRF trusted origins
_default_csrf = "https://farzadseif.pythonanywhere.com"
_CSRF = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", _default_csrf)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _CSRF.split(",") if o.strip()]

# Relax for local dev
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ]

# ------------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # local apps
    "main",
    "blog",
    # third-party
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # custom templates dir
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    r = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": r.path.lstrip("/"),
            "USER": r.username,
            "PASSWORD": r.password,
            "HOST": r.hostname,
            "PORT": r.port or "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE = "en"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Tehran")
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# Email (Gmail SMTP if USE_ANYMAIL=False)
# ------------------------------------------------------------------------------

USE_ANYMAIL = os.getenv("USE_ANYMAIL", "False").lower() == "true"

if USE_ANYMAIL:
    INSTALLED_APPS += ["anymail"]
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY", ""),
        "MAILGUN_SENDER_DOMAIN": os.getenv("MAILGUN_DOMAIN", ""),
    }
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", f"no-reply@{os.getenv('MAILGUN_DOMAIN','')}")
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").strip().lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "no-reply@safecode.local"

# ------------------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------------------

LOGIN_URL = "/accounts/login/"

# ------------------------------------------------------------------------------
# Security - Production only
# ------------------------------------------------------------------------------

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False

# ------------------------------------------------------------------------------
# Default PK
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
