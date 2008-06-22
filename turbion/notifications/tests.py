# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.test import TestCase
from django.db import models
from django.db.models import signals
from django.core.management import call_command
from django.core import mail

from turbion.notifications import EventDescriptor
from turbion.profiles.models import Profile
from turbion.visitors.models import User

class Owner( models.Model ):
    name = models.CharField( max_length = 50 )

class Animal( models.Model ):
    owner = models.ForeignKey( Owner )
    name = models.CharField( max_length = 50 )

class AnimalAdd( EventDescriptor ):
    class Meta:
        name = "Test Event"
        trigger = ( Animal, signals.post_save )

        link_model  = Owner
        link = lambda animal: animal.owner

class NotifTestCase( TestCase ):
    fixtures = [ "profiles", "dbtemplates" ]

    def setUp( self ):
        self.profile = Profile.objects.get( username = "daev" )
        self.user, created = User.objects.get_or_create_for( self.profile )

        self.owner = Owner.objects.create( name = "Sam" )

    def test_model_notif( self ):
        AnimalAdd.subscribe( self.user, self.owner )

        anim = Animal.objects.create( owner = self.owner, name = "dog" )

        self.assertEqual(len(mail.outbox), 1)

    def test_model_notif_another_obj( self ):
        AnimalAdd.subscribe( self.user, self.owner )

        owner = Owner.objects.create( name = "Dave" )
        anim = Animal.objects.create( owner = owner, name = "dog" )

        self.assertEqual(len(mail.outbox), 0)

    def test_unsubscribe( self ):
        from django.core.urlresolvers import reverse

        AnimalAdd.subscribe( self.user, self.owner )

        url, data = AnimalAdd.get_unsubscribe_url( self.user, self.owner ).split( "?" )

        response = self.client.get( url, dict( d.split( '=' ) for d in data.split( '&' ) ) )

        self.assertEqual( response.status_code, 200 )

        self.assert_( not AnimalAdd.has_subscription( self.user, self.owner ) )
