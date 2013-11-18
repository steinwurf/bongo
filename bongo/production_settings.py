"""
Django production settings for bongo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from settings import *
import os

DEBUG = False

TEMPLATE_DEBUG = False

TEMPLATE_DIRS += [os.path.join(STATIC_ROOT, 'files')]

# WARNING! FIX THIS!
ALLOWED_HOSTS = ['*']

SECRET_KEY = None
try:
   with open('SECRET', 'r') as secret_key_file:
    SECRET_KEY = secret_key_file.read()
except IOError:
    SECRET_KEY = 'testing'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
