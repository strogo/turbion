from django import template
from django.conf import settings

from turbion.bits.utils.urls import uri_reverse

register = template.Library()

@register.simple_tag
def server_tag():
    return '<link rel="openid.server" href="%(url)s"><link rel="openid2.provider" href="%(url)s">' % {'url': uri_reverse("turbion_openid_endpoint")}

@register.simple_tag
def delegate_tag():
    return '<link rel="openid.delegate" href="%s">' % settings.TURBION_OPENID_IDENTITY_URL
