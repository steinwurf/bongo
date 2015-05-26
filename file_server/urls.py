#! /usr/bin/env python
# encoding: utf-8
from django.conf.urls import url
from django.template import engines
from . import views


def include_file_server(root, namespace, wrapper=lambda func: func):
    """
    Create list of urls patterns to be included.

    :param namespace: Instance namespace for the URL entries being included.
    :param root: The root of the files to host.
    """
    engines.all()[0].dirs.append(root)

    urlpatterns = []

    urlpatterns.append(url(
        r'^/(?P<item>.+)$',
        lambda request, item: wrapper(
            views.show)(request, root, item), name="show"))

    urlpatterns.append(url(
        r'^$',
        lambda request: wrapper(
            views.show)(request, root), name="show"))
    # (urls, app_name, namespace)
    return (urlpatterns, 'file_server', namespace)
