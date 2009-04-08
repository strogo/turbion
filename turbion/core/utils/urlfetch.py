import httplib2

from django.conf import settings
from django.utils.http import urlencode

class ResponseObject(object):
    def __init__(self, status_code, content, headers={}):
        self.status_code = status_code
        self.content = content
        self.headers = headers

class UrlFetcher(object):
    def fetch(self, url, data=None, headers=None, timeout=10):
        http = httplib2.Http(timeout=timeout)

        if headers is None:
            headers = {}

        method = data and 'POST' or 'GET'
        data = data and urlencode(data) or ''

        resp, content = http.request(
            url, method, data, headers=headers
        )

        return ResponseObject(resp["status"], content, resp)

def _get_fetcher():
    fetcher = getattr(settings, "TURBION_URLFETCHER", UrlFetcher)

    if isinstance(fetcher, basestring):
        module, name = fetcher.rsplit(".", 1)
        mod = __import__(module, {}, {}, [''])

        fetcher = getattr(mod, name)

    if callable(fetcher):
        fetcher = fetcher()

    return fetcher

def fetch(url, data=None, headers=None, timeout=10):
    fetcher = _get_fetcher()

    return fetcher.fetch(url, data, headers)
