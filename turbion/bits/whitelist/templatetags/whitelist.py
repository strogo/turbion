from django import template
from django.conf import settings

from turbion.bits.utils.urls import uri_reverse

register = template.Library()

@register.simple_tag
def whitelist():
    return '<link rel="whitelist" href="%(url)s">' % {'url': uri_reverse("turbion_whitelist")}
