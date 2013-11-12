"""
Django settings for bongo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Set this to the parent folder for the folder named files, containing the files
# to serve.
FILE_DIR = BASE_DIR


IMAGE_TYPES = ['png', 'jpg', 'gif']

IMAGE_TYPES = [image.lower() for image in IMAGE_TYPES]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+jeqyau%4!8jlqcmgls)y9uo*xjd*sk56*tf(htak*xk-r45^y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'file_server',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bongo.urls'

WSGI_APPLICATION = 'bongo.wsgi.application'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',)

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = { }

# Cache
# https://docs.djangoproject.com/en/1.3/ref/settings/#std:setting-CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/bongo_cache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = '/var/www/bongo/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Bongo related static files
    os.path.join(BASE_DIR, "static"),
    # Twitter Bootstrap stuff
    os.path.join(BASE_DIR, "bootstrap/dist"),
    os.path.join(BASE_DIR, "bootstrap/assets"),
    # Files
    os.path.join(FILE_DIR, "files"),
)
