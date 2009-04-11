from django import template
from django.conf import settings

from turbion.core.utils.urls import uri_reverse

register = template.Library()

@register.simple_tag
def server_tag():
    return '<link rel="openid.server" href="%s">' % uri_reverse("turbion_openid_endpoint")

@register.simple_tag
def delegate_tag():
    return '<link rel="openid.delegate" href="%s">' % settings.TURBION_OPENID_IDENTITY_URL
