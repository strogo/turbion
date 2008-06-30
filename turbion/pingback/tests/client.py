# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.dispatch import dispatcher
from django.db import models

from turbion.pingback import client, utils, signals
from turbion.pingback.tests.utils import TestTransport

from pantheon.utils.urlfetch import UrlFetcher, ResponseObject

settings.PINGBACK_TRANSPORT = TestTransport

TITLE = ""
PARAGRAPH = "Вот параграф со ссылкой на пост с длинной строчкой"
ENTRY_TEXT = """<p>Вот первый параграф</p>

<p>Вот параграф со ссылкой <a href="%s">на пост</a> с длинной строчкой</p>

<p>Третий параграф</p>
"""

TARGET_URI = "http://foobar.com"

ENTRY_TEXT = ENTRY_TEXT % TARGET_URI

REMOTE_HTML = """<html><link rel="pingback" href="http://foobar.com/pingback/xmlrpc/pingback.testentry/" /></head></html>"""

class TestEntry( models.Model ):
    text = models.TextField()

    class Meta:
        app_label = "pingback"

    def get_absolute_url( self ):
        return "/entry/%s/" % self.id

    def process( self ):
        dispatcher.send( signal  = signals.send_pingback,
                        sender   = self.__class__,
                        instance = self,
                        url      = self.get_absolute_url(),
                        text     = self.text,
                )

class MyFetcher( UrlFetcher ):
    mapping = { "http://foobar.com" : ( 200, {}, REMOTE_HTML ) }

    fetched = []

    def fetch( self, url, data ):
        self.fetched.append( url )

        for mapped_url, data in self.mapping.iteritems():
            if url.startswith( mapped_url ):
                return ResponseObject( data[ 0 ], data[ 2 ], data[ 1 ] )

        return super( MyFetcher, self ).fetch( url, data )

my_fetcher = MyFetcher()

settings.PANTHEON_URLFETCHER = my_fetcher

class ClientTest( TestCase ):
    fixtures = ["test/auth", "test/pingback"]

    def setUp(self):
        site = Site.objects.get_current()
        site.domain = "to.com"
        site.save()

        self.entry = TestEntry.objects.create( text = ENTRY_TEXT )

        self.entry.process()

    def test_outgoing(self):
        from turbion.pingback.models import Outgoing

        self.assertEqual( Outgoing.objects.count(), 1 )

        out = Outgoing.objects.get()
        self.assertEqual( out.object,     self.entry )
        self.assertEqual( out.target_uri, TARGET_URI )
