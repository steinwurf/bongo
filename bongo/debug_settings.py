#! /usr/bin/env python
# encoding: utf-8
"""
Django debug settings for bongo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from settings import *

DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS += [os.path.join(BASE_DIR, 'files')]

SECRET_KEY = 'SSSHVERYSECRET!'
