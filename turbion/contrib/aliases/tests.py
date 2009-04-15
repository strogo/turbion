from django.test import TestCase
from django import http

from turbion.contrib.aliases.models import Alias

class SimpleAliasTest(TestCase):
    fixtures = ["turbion/test/blogs"]

    def setUp(self):
        self.blog = Blog.objects.all()[0]

        self.alias = Alias.objects.create(
            blog=self.blog,
            from_url="/tags/",
            to_url="/bar/foo/",
            status_code=Alias.status_codes.permanent
        )

    def test_redirect(self):
        response = self.client.get(self.alias.from_url)

        self.assertEqual(response.status_code, http.HttpResponsePermanentRedirect.status_code)
        self.assertEqual(response["Location"], "http://testserver" + self.alias.to_url)

class ExcludeAgentAliasTest(TestCase):
    fixtures = ["turbion/test/blogs"]

    def setUp(self):
        self.blog = Blog.objects.all()[0]

        self.alias = Alias.objects.create(
            blog=self.blog,
            from_url="/tags/",
            to_url="/bar/foo/",
            status_code=Alias.status_codes.permanent,
            exclude_user_agent=Alias.user_agents.feedburner
        )

    def test_redirect(self):
        response = self.client.get(self.alias.from_url, HTTP_USER_AGENT="foobar")

        self.assertEqual(response.status_code, http.HttpResponsePermanentRedirect.status_code)
        self.assertEqual(response["Location"], "http://testserver" + self.alias.to_url)

    def test_not_redirect(self):
        response = self.client.get(self.alias.from_url, HTTP_USER_AGENT="feedburner")

        self.assert_(response.status_code in (http.HttpResponse.status_code, 404))
