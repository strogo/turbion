from django.test import TestCase, Client
from django import http
from django.conf import settings
from django.core.handlers import wsgi, base

class RequestFactory(Client):
    def __init__(self):
        Client.__init__(self)

        self._handler = base.BaseHandler()
        self._handler.load_middleware()
        self._session = {}

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
    credentials = {'username': "test", 'password': "test"}

    def assertResponseStatus(self, response, status=http.HttpResponse.status_code):
        self.assertEqual(response.status_code, status)

    def assertStatus(self, url, status=http.HttpResponse.status_code, data={}, method="get"):
        response = getattr(self.client, method)(url, data=data)

        self.assertResponseStatus(response, status)

        return response

    def hack_captcha(self, response):
        if isinstance(response, http.HttpRequest):
            request = response
        else:
            request = response.request

        if isinstance(request, dict):
            session = self._get_session(response.cookies)
        else:
            session = request.session

        if "turbion_captcha" in session:
            values = session["turbion_captcha"].values()
            values.sort(lambda a, b: a[1] > b[1])
            solution = values[0][0].solutions[0]

            return {
                "captcha_0": session["turbion_captcha"].keys()[0],
                "captcha_2": solution
            }

        return {}

    def _get_session(self, cookies):
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        session_key = cookies.get(settings.SESSION_COOKIE_NAME, None).value

        return engine.SessionStore(session_key)

    def login(self):
        result = self.client.login(**self.credentials)
        self.assert_(result, "Cannot login")

    @property
    def user(self):
        from turbion.core.profiles.models import Profile
        return Profile.objects.get(username=self.credentials["username"])
