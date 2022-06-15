import os
from .common import *
import django_on_heroku
import dj_database_url


SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = ["https://peers-app-sh.herokuapp.com"]

DATABASES = {
    "default": dj_database_url.config()
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Configure Django App for Heroku.
django_on_heroku.settings(locals())
