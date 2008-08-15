# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

import os

register = template.Library()

@register.simple_tag
def add_css(path):
    return '<link href=\"%scss/%s\" media=\"screen\"\
             rel=\"stylesheet\" type=\"text/css\"/>' % (settings.MEDIA_URL, path)

@register.simple_tag
def add_admin_css(path):
    return '<link href=\"%scss/%s\" media=\"screen\"\
             rel=\"stylesheet\" type=\"text/css\"/>' % (settings.ADMIN_MEDIA_PREFIX, path)

@register.simple_tag
def add_js(path):
    return '<script type="text/javascript" src="%sjs/%s"></script>' % (settings.MEDIA_URL, path)

def generic_feed(type, title, path):
    return '<link rel="alternate" type="%s" title="%s" href="%s">' % (type, title, path)

@register.simple_tag
def atom_feed(title, path):
    return generic_feed('application/atom+xml', title, path)