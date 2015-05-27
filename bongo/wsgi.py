#! /usr/bin/env python
# encoding: utf-8
"""Web Server Gateway Interface."""
import os
import sys
from django.core.wsgi import get_wsgi_application

# put the Django project on sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ["DJANGO_SETTINGS_MODULE"] = "bongo.production_settings"
application = get_wsgi_application()
