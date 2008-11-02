# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.sites.models import Site

from turbion.pingback.server import ping
from turbion.pingback.models import Incoming
from turbion.pingback.tests.utils import TestEntry, BASE_ENTRY_TEXT, test_fetcher,PARAGRAPH
from turbion.utils.descriptor import to_descriptor

class ServerTest( TestCase ):
    def setUp( self ):
        self.source_uri = "http://source.host.com"
        self.target_uri = "http://target.host.com"

        site = Site.objects.get_current()
        site.domain = self.target_uri[ self.target_uri.index( "//" ) + 2 : ]
        site.save()

        text = BASE_ENTRY_TEXT

        self.entry = TestEntry.objects.create( text = text % self.source_uri )

        test_fetcher.mapping[ self.source_uri ] = ( 200, {}, BASE_ENTRY_TEXT % ( self.target_uri + self.entry.get_absolute_url() ) )

        self.needed_status = 'Pingback from %s to %s%s registered. Keep the web talking! :-)' % ( self.source_uri, self.target_uri, self.entry.get_absolute_url(),  )

        dscr = to_descriptor(self.entry.__class__)

        ping( self.source_uri,
              self.target_uri + self.entry.get_absolute_url(),
              dscr,
              self.entry.id )

    def test_ping(self):
        self.assertEqual(Incoming.objects.count(), 1)

        inc = Incoming.objects.get()

        self.assertEqual( inc.status,    self.needed_status )
        self.assertEqual( inc.paragraph, "[...]%s[...]" % PARAGRAPH )
