"""
Django production settings for bongo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from settings import *

DEBUG = False

TEMPLATE_DEBUG = False

# WARNING! FIX ThIS!
ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ['SECRET_KEY']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
