# -*- coding: utf-8 -*-
from django.conf import settings

class ResponseObject(object):
    def __init__(self, status_code, content, headers={}):
        self.status_code = status_code
        self.content = content
        self.headers = headers

class UrlFetcher(object):
    def fetch(self, url, data=None):
        from urllib2 import urlopen
        inp = urlopen(url)

        return ResponseObject(inp.code, inp.read(), inp.headers)

def _get_fetcher():
    fetcher = getattr(settings, "TURBION_URLFETCHER", UrlFetcher)

    if isinstance(fetcher, basestring):
        module, name = fetcher.rsplit(".", 1)
        mod = __import__(module, {}, {}, [''])

        fetcher = getattr(mod, name)

    if callable(fetcher):
        fetcher = fetcher()

    return fetcher

def fetch(url, data=None):
    fetcher = _get_fetcher()

    return fetcher.fetch(url, data)