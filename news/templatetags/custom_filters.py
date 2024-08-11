import re
from django import template

register = template.Library()

@register.filter(name='boldify')
def boldify(value):
    """
    Replaces **text** with <strong>text</strong>.
    """
    # Regular expression to find text surrounded by **
    pattern = r'\*\*(.*?)\*\*'
    # Replace with <strong>text</strong>
    return re.sub(pattern, r'<strong>\1</strong>', value)

