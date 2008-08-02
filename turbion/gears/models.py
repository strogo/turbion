# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models

from pantheon.models.manager import GenericManager

class GearInfo( models.Model ):
    name = models.CharField( max_length = 150 )
    descriptor = models.CharField( max_length = 250, unique = True )

    interval = models.CharField( max_length = 250 )

    last = models.DateTimeField( null = True )
    next = models.DateTimeField( null = True, db_index = True )

    is_active = models.BooleanField( default = True )
    is_lost = models.BooleanField( default = False )

    objects = models.Manager()
    active = GenericManager( is_active = True, is_lost = False )

    def has_revolved( self ):
        now = datetime.now()

        self.last = now

        interval = int( self.interval )

        self.next = now + timedelta( minutes = interval )

        self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "turbion_gear"
