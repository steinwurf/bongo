#! /usr/bin/env python
# encoding: utf-8
"""Handle urls."""
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'bongo.views.index', name='index'),
    url(r'^about$', 'bongo.views.about', name='about'),
    url(r'^files', include('file_server.urls')),
)
