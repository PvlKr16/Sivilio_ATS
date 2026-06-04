"""
Django settings for HR IT platform.
"""

import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _   # ← ДОБАВЛЕНО

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='dev-secret-key-change-me')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000",]

CLOUDFLARE_URL = os.environ.get("CLOUDFLARE_URL", "")
if CLOUDFLARE_URL:
    CSRF_TRUSTED_ORIGINS.append(CLOUDFLARE_URL)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    # Local apps
    'apps.accounts',
    'apps.core',
    'apps.people',
    'apps.companies',
    'apps.vacancies',
    'apps.events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',      # ← после SessionMiddleware, до CommonMiddleware ✓
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'hr_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.sidebar_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'hr_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='hrdb'),
        'USER': config('POSTGRES_USER', default='hruser'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='hrpassword'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Auth
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ['apps.accounts.backends.EmailBackend']
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('be', _('Беларуская')),
    ('de', _('Deutsch')),
    ('en', _('English')),
    ('pl', _('Polski')),
    ('ru', _('Русский')),
    ('uk', _('Українська')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT', default=BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT', default=BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Pagination
PAGE_SIZE = 15
