from django import template

register = template.Library()

def format(value, arg):
    """
    Alters default filter "stringformat" to not add the % at the front,
    so the variable can be placed anywhere in the string.
    """
    try:
        if value:
            return (unicode(arg)) % value
        else:
            return u''
    except (ValueError, TypeError):
        return u''
register.filter('format', format)