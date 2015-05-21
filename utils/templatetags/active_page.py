#! /usr/bin/env python
# encoding: utf-8

from django import template
import re

register = template.Library()


@register.simple_tag
def active(request, pattern):
    """Return the string active if the pattern is in the requested path."""
    if type(request) is not str and re.search(pattern, request.path):
        return 'active'
    return ''
