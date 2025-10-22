# accounts/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a string with another string
    Usage: {{ value|replace:"old,new" }}
    """
    if not value or not arg:
        return value
    
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except (ValueError, AttributeError):
        return value

@register.filter
def with_space(value):
    """
    Replaces underscores with spaces and capitalizes each word
    Usage: {{ value|with_space }}
    """
    if not value:
        return value
    
    try:
        return value.replace('_', ' ').title()
    except AttributeError:
        return value

@register.filter
def get_icon_for_mode(mode):
    """
    Returns appropriate icon for consultation mode
    """
    icon_map = {
        'video_call': 'video',
        'phone_call': 'phone',
        'in_person': 'building'
    }
    return icon_map.get(mode, 'calendar-alt')

@register.filter
def get_status_class(status):
    """
    Returns appropriate CSS class for status
    """
    class_map = {
        'scheduled': 'bg-blue-100 text-blue-800',
        'completed': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
    }
    return class_map.get(status, 'bg-gray-100 text-gray-800')