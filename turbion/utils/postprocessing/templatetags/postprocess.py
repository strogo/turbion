# -*- coding: utf-8 -*-
from django import template

from turbion.utils.postprocessing import ProcessorSpot

register = template.Library()

def wrap(method):
    def _inner(value):
        if value is None:
            value = ""
        return method(value)
    return _inner

for name, func in ProcessorSpot.processors.iteritems():
    register.filter(name.rsplit(".",2)[1], wrap(func.postprocess))

@register.filter
def postprocess(instance, field, processor="postprocess"):
    val = getattr(instance, field)
    return getattr(instance, processor).postprocess(val)

@register.filter
def sanitize(value):
    from BeautifulSoup import BeautifulSoup, Comment
    valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
    valid_attrs = 'href src'.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                     if attr in valid_attrs]
    return soup.renderContents().decode('utf8').replace('javascript:', '')
