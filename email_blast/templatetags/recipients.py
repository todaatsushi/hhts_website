from django import template

register = template.Library()

@register.filter
def to_list(value):
    """
    Changes literal string of a list into an actual list.
    """
    return value.split(',')
