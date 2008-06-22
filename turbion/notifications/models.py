# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from turbion.visitors.models import User

from pantheon.models.models import ActionModel

class EventManager( models.Manager ):
    pass

class Event( models.Model ):
    descriptor = models.CharField( max_length = 250, unique = True )

    template = models.CharField( max_length = 250, null = True, blank = True )
    subject_title = models.CharField( max_length = 250 )

    def __unicode__(self):
        return self.descriptor

    class Meta:
        verbose_name = "событие"
        verbose_name_plural = "события"

class Connection( ActionModel, models.Model ):
    event = models.ForeignKey( Event )
    user = models.ForeignKey( User, related_name="notification_recipient" )

    connection_ct = models.ForeignKey( ContentType, null = True  )
    connection_id = models.PositiveIntegerField( null = True )

    connection = GenericForeignKey( "connection_ct", "connection_id" )

    def __unicode__(self):
        return "%s: %s" % ( self.event.name, self.object_id )

    class Meta:
        verbose_name = "соединение"
        verbose_name_plural = "соединения"

        unique_together = [ ( "event", "user", "connection_ct", "connection_id" ) ]
