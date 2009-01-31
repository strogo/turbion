# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.test import TestCase
from django.conf import settings

from turbion.pingback import signals
from turbion.utils.urlfetch import UrlFetcher, ResponseObject

class TestEntry(models.Model):
    text = models.TextField()

    class Meta:
        app_label = "pingback"

    def get_absolute_url(self):
        return "/entry/%s/" % self.id

    def process(self):
        signals.send_pingback.send(
                        sender   = self.__class__,
                        instance = self,
                        url      = self.get_absolute_url(),
                        text     = self.text,
                )


TITLE = ""
PARAGRAPH = "This is paragraph with link to large post"
BASE_ENTRY_TEXT = """<p>This is first pragraph</p>
                  <p>This is paragraph with link <a href="%s">to large post</a></p>
                  <p>Third paragraph</p>"""

REMOTE_HTML = "<html><link rel=\"pingback\" href=\"http://foobar.com/pingback/xmlrpc/pingback.testentry/\" /></head></html>"

class TestFetcher(UrlFetcher):
    mapping = {"http://target.host.com": (200, {}, REMOTE_HTML)}

    fetched = []

    def fetch(self, url, data):
        self.fetched.append(url)

        for mapped_url, data in self.mapping.iteritems():
            if url.startswith(mapped_url):
                return ResponseObject(data[0], data[2], data[1])

        return super(MyFetcher, self).fetch(url, data)

test_fetcher = TestFetcher()

settings.TURBION_URLFETCHER = test_fetcher
