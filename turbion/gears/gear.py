# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.db.models import Q

from turbion.gears.models import GearInfo

class GearSpot( type ):
    def __new__( cls, name, bases, attrs ):
        try:
            Gear
            skip = False
        except NameError:
            cls.gears = {}
            skip = True

        if not skip and attrs.get( 'register', True ):
            gear = type.__new__( cls, name, bases, attrs )

            gear.descriptor = "%s.%s" % ( cls.__module__, name )

            cls.gears[ gear.descriptor ] = gear()
            return gear

        return super( GearSpot, cls ).__new__( cls, name, bases, attrs )

    @classmethod
    def sync( cls ):
        for descriptor, gear in cls.gears.iteritems():
            gear_info, created = GearInfo.objects.get_or_create( descriptor = descriptor,
                                                                 defaults = { "name"     : gear.name,
                                                                              "interval" : gear.every } )

    @classmethod
    def revolve_all( cls ):
        cls.sync()

        for gear_info in GearInfo.active.filter( Q( next__lte = datetime.now() ) | Q( next = None ) ):
            try:
                gear = cls.gears[ gear_info.descriptor ]
            except KeyError:
                gear_info.is_lost = True
                gear_info.save()
                continue

            try:
                gear.activity()
                gear_info.has_revolved()
            except Exception, e:
                pass

class Gear( object ):
    __metaclass__ = GearSpot

    name = "Gear"
    every = 1

    def activity( self ):
        raise NotImplementedError

class CommendGear( Gear ):
    register = False

    command_args = []
    commands_options = {}

    def activity( self ):
        from django.core.management import call_command

        call_command( self.command, *self.command_args, **self.commands_options )
