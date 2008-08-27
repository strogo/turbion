# -*- coding: utf-8 -*-
from django.test import TestCase
from django import http

from turbion.aliases.models import Alias

class SimpleTest(TestCase):
    def setUp(self):
        self.alias = Alias.objects.create(from_url="/foo/bar/",
                                     to_url="/bar/foo/",
                                     status_code=Alias.status_codes.permanent)

    def test_redirect(self):
        response = self.client.get(self.alias.from_url)

        self.assertEqual(response.status_code, http.HttpResponsePermanentRedirect.status_code)
        self.assertEqual(response["Location"], "http://testserver" + self.alias.to_url)

class ExcludeTest(TestCase):
    def setUp(self):
        self.alias = Alias.objects.create(from_url="/",
                                     to_url="/bar/foo/",
                                     status_code=Alias.status_codes.permanent,
                                     exclude_user_agent=Alias.user_agents.feedburner)

    def test_redirect(self):
        response = self.client.get(self.alias.from_url, HTTP_USER_AGENT="foobar")

        self.assertEqual(response.status_code, http.HttpResponsePermanentRedirect.status_code)
        self.assertEqual(response["Location"], "http://testserver" + self.alias.to_url)

    def test_not_redirect(self):
        response = self.client.get(self.alias.from_url, HTTP_USER_AGENT="feedburner")

        self.assertEqual(response.status_code, http.HttpResponse.status_code)
