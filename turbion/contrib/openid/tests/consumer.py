# -*- coding: utf-8 -*-
import tempfile

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

from turbion.openid.tests import utils

class BaseOpenidConsumerTest(object):
    def setUp(self):
        from processing import Process
        from turbion.openid.tests import test_server

        self.process = Process(target=test_server.main,
                               args=(
                                    settings.TURBION_TEST_OPENID_SERVER_HOST,
                                    settings.TURBION_TEST_OPENID_SERVER_PORT,
                                    tempfile.mkdtemp("openid_test")
                                )
                        )
        self.process.start()

    def tearDown(self):
        import time
        time.sleep(1)
        self.process.terminate()

class OpenidFormTest(BaseOpenidConsumerTest, TestCase):
    def test_form_submit(self):
        data = {"openid": utils.identity_url}
        response = self.client.post(reverse("openid_login"), data=data)

        self.assertEqual(response.status_code, 302)
        self.assert_(response["Location"].startswith("http://%s:%s/" % (utils.host, utils.port)))

class OpenidAuthenticationTest(TestCase):
    def setUp(self):
        self.server = utils.FakeServer(utils.identity_url)

    def _strip_host(self, url):
        from urlparse import urlsplit
        from cgi import parse_qs
        path, query = urlsplit(url)[2:4]

        return path, parse_qs(query)

    def test_good_authentication(self):
        url, data = self._strip_host(self.server.get_allow_auth_url())
        print data
        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("openid_collect"))

    def test_bad_authentication(self):
        pass
