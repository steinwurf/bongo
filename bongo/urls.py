#! /usr/bin/env python
# encoding: utf-8
"""Handle urls."""
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings

import file_server.urls
import os


if settings.DEBUG:
    root = settings.BASE_DIR
else:
    root = settings.STATIC_ROOT

public_root = os.path.join(root, 'public')
private_root = os.path.join(root, 'private')

urlpatterns = patterns(
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', 'bongo.views.index', name='index'),
    url(r'^about$', 'bongo.views.about', name='about'),
    url(r'^files/public',
        file_server.urls.include_file_server(
            public_root, "public")),
    url(r'^files/private',
        file_server.urls.include_file_server(
            private_root, "private", login_required)),
    url(r'^logout/$', 'bongo.views.logout'),
)
