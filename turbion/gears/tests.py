# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from django.conf import settings

from turbion.gears import Gear, GearSpot
from turbion.gears.models import GearInfo

class TestCounter( object ):
    def __init__( self ):
        self.count = 0

    def touch( self ):
        self.count += 1

    def clear( self ):
        self.count = 0

counter = TestCounter()

class TestGear( Gear ):
    every = 1

    def activity( self ):
        counter.touch()

class GearTest( TestCase ):
    def tearDown( self ):
        counter.clear()

    def test_registered_gear( self ):
        self.assertEqual( len( GearSpot.gears ), 1 )

    def test_gear_activity( self ):
        TestGear().activity()
        self.assertEqual( counter.count, 1 )

    def test_command( self ):
        from django.core.management import call_command

        call_command( "revolvegears" )
        now = datetime.now()

        self.assertEqual( counter.count, 1 )

        info = GearInfo.objects.all()[ 0 ]

        self.assert_( info.next )
        self.assert_( info.last )

        self.assert_( info.next < now + timedelta( minutes = TestGear.every ) )

    def test_feed( self ):
        from django.core.urlresolvers import reverse

        feed_url = reverse( "gears_feed", args = ( "latest", ) )

        response = self.client.get( feed_url )

        self.assertEqual( response.status_code, 200 )
