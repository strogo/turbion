# -*- coding: utf-8 -*-
from django import template

from turbion.utils.urls import uri_reverse

register = template.Library()

rel_map = {
    "1": "openid.server",
    "2": "openid2.provider",
}

@register.simple_tag
def openid_server(version="2"):
    return '<link rel="%s" href="%s">' % (rel_map.get(str(version), "2"),
                                          uri_reverse("turbion_openid_endpoint"))

