# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.db import models

from turbion.pingback import client, signals
from turbion.pingback.tests.utils import TestEntry, BASE_ENTRY_TEXT

class TestServerProxy(client.ServerProxy):
    """
        Mock server proxy class.
        Returns string as status with method name and params
    """
    def __request(self, methodname, params):
        return "%s%s" % (methodname, params)

    def __getattr__(self, name):
        import xmlrpclib
        return xmlrpclib._Method(self.__request, name)

client.ServerProxy = TestServerProxy

class ClientTest(TestCase):
    def setUp(self):
        self.source_uri = "http://source.host.com"
        self.target_uri = "http://target.host.com"

        site = Site.objects.get_current()
        site.domain = self.source_uri[self.source_uri.index("//") + 2:]
        site.save()

        text = BASE_ENTRY_TEXT

        self.entry = TestEntry.objects.create(text=text % self.target_uri)

        self.needed_status = "pingback.ping('%s%s', u'%s')" % (
                                            self.source_uri,
                                            self.entry.get_absolute_url(),
                                            self.target_uri
                                    )

        self.entry.process()

    def test_outgoing(self):
        from turbion.pingback.models import Outgoing

        self.assertEqual(Outgoing.objects.count(), 1)

        out = Outgoing.objects.get()
        self.assertEqual(out.object,     self.entry)
        self.assertEqual(out.target_uri, self.target_uri)
        self.assertEqual(out.status,     self.needed_status)
