import random
import string
from django import template

register = template.Library()

@register.simple_tag
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    rstr = ''.join(random.choice(letters) for i in range(stringLength))
    return rstr
