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

from turbion.pingback import client, signals
from turbion.pingback.tests.utils import TestEntry, BASE_ENTRY_TEXT

class ClientTest( TestCase ):
    def setUp( self ):
        self.source_uri = "http://source.host.com"
        self.target_uri = "http://target.host.com"
        
        site = Site.objects.get_current()
        site.domain = self.source_uri[ self.source_uri.index( "//" ) + 2 : ]
        site.save()
        
        text = BASE_ENTRY_TEXT

        self.entry = TestEntry.objects.create( text = text % self.target_uri )
            
        self.needed_status = 'Pingback from %s%s to %s registered. Keep the web talking! :-)' % ( self.source_uri, self.entry.get_absolute_url(), self.target_uri )
        
        self.old_ping = client.call_ping
        client.call_ping = lambda gateway, source_uri, target_uri: 'Pingback from %s to %s registered. Keep the web talking! :-)' % ( source_uri, target_uri )
            
        self.entry.process()
        
    def tearDown( self ):
        client.call_ping = self.old_ping

    def test_outgoing(self):
        from turbion.pingback.models import Outgoing

        self.assertEqual( Outgoing.objects.count(), 1 )

        out = Outgoing.objects.get()
        self.assertEqual( out.object,     self.entry )
        self.assertEqual( out.target_uri, self.target_uri )
        self.assertEqual( out.status,     self.needed_status )
