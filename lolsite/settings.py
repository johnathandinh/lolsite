"""
Django settings for lolsite project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
import pathlib
from decouple import config
import logging


logger = logging.getLogger(__name__)


SECRET_KEY = config(
    "LOLSITE_SECRET_KEY", "6cs%&oj!lvxpvj44r63-#ie=-%er1hs@%sbt1k9=lf7-b_mlxv"
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'lolsite.helpers.Paginator'
}

if config("LOLSITE_HOST", None) == "dev":
    from lolsite.settingsenv.dev_settings import *
    print('Using local dev settings.')
elif config("ENVNAME", None) == "test":
    from lolsite.settingsenv.settings_test import *
    print('Using circle ci settings.')
elif config('ENVNAME', None) == 'fly':
    from lolsite.settingsenv.fly_settings import *
else:
    raise RuntimeError('ENVNAME or LOLSITE_HOST must be set.')

GIT_BUILD = 0
try:
    with open(os.path.join(BASE_DIR, ".git", "logs", "HEAD")) as git_log:
        line = [line for line in git_log][-1]
        GIT_BUILD = line.split()[1][:7]
except:
    try:
        with open(pathlib.PurePath(BASE_DIR, "gitbuild")) as git_log:
            GIT_BUILD = git_log.read().strip()
    except:
        pass

VERSION = [0, 1, GIT_BUILD]
VERSION_STRING = ".".join(list(map(str, VERSION)))


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "storages",
    'core',
    "lolsite",
    "data",
    "match",
    "player",
    "fun",
    "pro",
    "notification",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lolsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "lolsite.context_processors.version_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "lolsite.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = []
try:
    STATICFILES_DIRS += [
        os.path.join(BASE_DIR, "react", "build", "static"),
    ]
except:
    logger.warning('Could not add react/build/static to staticfilesdirs.')


CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


# SENDGRID CONNECTION
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = config("LOLSITE_EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "brianjp93@gmail.com"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
