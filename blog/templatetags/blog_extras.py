from django import template

register = template.Library()

@register.filter
def get_image_url(image_field, default_url=None):
    """
    Safely get image URL from ImageField.
    Usage: {{ post.image|get_image_url:"default/image.jpg" }}
    """
    if image_field and hasattr(image_field, 'url'):
        return image_field.url
    return default_url or '/static/images/default-blog-image.jpg'

@register.filter
def truncate_chars(value, max_length):
    """
    Truncate a string after a certain number of characters.
    """
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value