from django import template
from django.conf import settings

from turbion.bits.utils.title import gen_title

register = template.Library()

@register.simple_tag
def make_title(page, section=None, site=None):
    bits = {
        "page": page,
    }
    if section:
        bits.update({"section": section})
    if site:
        bits.update({"site": site})

    return gen_title(bits)
