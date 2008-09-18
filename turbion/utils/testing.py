# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django import http

from django.core.handlers import wsgi, base

class RequestFactory(Client):
    def __init__(self):
        Client.__init__(self)

        self._handler = base.BaseHandler()
        self._handler.load_middleware()

    def apply_middleware(self, request):
        for middleware_method in self._handler._request_middleware:
            response = middleware_method(request)
            if response:
                raise RuntimeError("process_request middleware method returns response")

    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)

        request = wsgi.WSGIRequest(environ)
        self.apply_middleware(request)

        return request

class BaseViewTest(TestCase):
    def assertStatus(self, url, status=http.HttpResponse.status_code, data={}):
        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, status)

        return response

    def hack_captcha(self, response, field_name="captcha"):
        HASH_RE = re.compile("name=\"%s_0\" value=\"(\w+)\"" % field_name)

        manager = CaptchaManager(response.request)

        m = HASH_RE.search(response.content)
        if m:
            hash = m.groups()[0]

            test = manager.factory.get(hash)
            captcha = test.solutions[0]
        else:
            captcha = ""
            hash = ""

        return {
            "%s_0" % field_name: hash,
            "%s_2" % field_name: captcha
        }
