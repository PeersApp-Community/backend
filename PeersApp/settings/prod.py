import os
from .common import *, DEBUG
import django_on_heroku
import dj_database_url


SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ["DEBUG"]
# print(DEBUG)
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

# Configure Django App for Heroku.
django_on_heroku.settings(locals())
# https://peers-app-sh.herokuapp.com/
