# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls.defaults import url

MULTIPLE_SETUP = settings.TURBION_BLOGS_MULTIPLE

def blog_reverse(viewname, urlconf=None, args=None, kwargs=None):
    if not MULTIPLE_SETUP:
        if args:
            args = list(args)
            del args[0]
        elif kwargs:
            kwargs.pop("blog", None)

    url = reverse(viewname, urlconf, args, kwargs)

    return url.replace("?", "")

def permalink(func):
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return blog_reverse(bits[0], None, *bits[1:3])
    return inner

if MULTIPLE_SETUP:
    blog_slug = r"^(?P<blog>[\w_-]+)/"
else:
    blog_slug = r"^"

def blog_url(regex, view, kwargs=None, name=None, prefix=''):
    return url(blog_slug + regex, view, kwargs, name, prefix)
