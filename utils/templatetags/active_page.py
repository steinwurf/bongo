from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if type(request) is not str and re.search(pattern, request.path):
        return 'active'
    return ''