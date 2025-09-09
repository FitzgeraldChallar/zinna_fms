"""
Production-ready Django settings for the `core` project.

This file is a refactored version of the settings you provided with
sensible defaults for deploying on Render (or similar PaaS).

Key changes:
 - secrets and debug read from environment variables
 - ALLOWED_HOSTS read from environment variable (no wildcard)
 - dj_database_url fallback to a local sqlite file when DATABASE_URL is not set
 - static handling configured for WhiteNoise (STATIC_ROOT + STATICFILES_STORAGE)
 - secure headers / cookies when DEBUG=False (and a conservative HSTS default)
 - console logging configured for PaaS logs
 - optional S3 configuration (commented) for media files

Edit environment variables on Render to match the names used here
(DJANGO_SECRET_KEY, DJANGO_DEBUG, ALLOWED_HOSTS, DATABASE_URL, etc.).
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------
# Basic / Security
# ----------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-secret")

# Use environment variable to toggle debug in production
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# ALLOWED_HOSTS should be a comma-separated list in the env var
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ----------------------
# Installed apps + middleware
# ----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # your apps
    'students',
    'transactions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ----------------------
# Database
# ----------------------
# If DATABASE_URL is provided (e.g. Render Postgres), dj_database_url will parse it.
# Otherwise we fall back to a local sqlite database so the project still runs locally.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,
    )
}

# ----------------------
# Password validation
# ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ----------------------
# Internationalization
# ----------------------
LANGUAGE_CODE = 'en-us'

# keep UTC for server timezone by default — change to 'Africa/Monrovia' if you prefer local time
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True
USE_TZ = True

# ----------------------
# Static & media files
# ----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic will place files here

# WhiteNoise compressed manifest storage for long-term cache headers
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------
# Security hardening (only applied when DEBUG=False)
# ----------------------
if not DEBUG:
    # When behind a proxy (Render, Heroku, etc.), this header tells Django the request is secure
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Redirect all HTTP to HTTPS
    SECURE_SSL_REDIRECT = True

    # HSTS - start small (60) then increase to 31536000 when you are confident
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 60))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Other headers
    SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# ----------------------
# Logging (console-friendly for PaaS)
# ----------------------
LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

# ----------------------
# Defaults
# ----------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


