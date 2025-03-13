from django import template
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value with the given argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0  # Return 0 if there is an error
