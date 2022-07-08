import os
from .common import *
import django_on_heroku
import dj_database_url


SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ.get("DEBUG", False)

DEBUG = True

ALLOWED_HOSTS = ["https://peers-app-sh.herokuapp.com"]

DATABASES = {"default": dj_database_url.config()}
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
# EMAIL_HOST_USER =os.environ['MAILGUN_SMTP_LOGIN']
# EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
# EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configure Django App for Heroku.
django_on_heroku.settings(locals())
# https://peers-app-sh.herokuapp.com/

# Debugging in heroku live
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "testlogger": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}


DEBUG_PROPAGATE_EXCEPTIONS = True
COMPRESS_ENABLED = os.environ.get("COMPRESS_ENABLED", False)
