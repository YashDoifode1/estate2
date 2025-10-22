from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def first_word(value):
    """Get the first word of a string"""
    return value.split(' ')[0] if value else ''

@register.filter
@stringfilter
def get_first_name(value):
    """Get the first name from a full name"""
    if value and ' ' in value:
        return value.split(' ')[0]
    return value