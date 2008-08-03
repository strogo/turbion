# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import dispatcher
from turbion.pingback import client, signals

from pantheon.utils.enum import Enum

class Incoming(models.Model):
    types = Enum( pingback  = "pingback",
                  trackback = "trackback" )

    type         = models.CharField( max_length = 10, choices = types, default = types.pingback )

    source_url   = models.URLField()
    target_url   = models.CharField( max_length=255 )

    date         = models.DateTimeField( default=datetime.now)
    status       = models.CharField( max_length=255 )

    title        = models.CharField( max_length=255, null = True )
    paragraph    = models.TextField( null = True )

    content_type = models.ForeignKey( ContentType, null = True, blank = True )
    object_id    = models.PositiveIntegerField( null = True, blank = True )
    object       = generic.GenericForeignKey()

    class Meta:
        verbose_name        = "входящий"
        verbose_name_plural = "входящие"
        unique_together     = ( ( "source_url", "content_type", "object_id" ), )
        db_table            = "turbion_pingback_incoming"

class Outgoing(models.Model):
    target_uri   = models.URLField()
    title        = models.CharField( max_length = 250 )
    rpcserver    = models.URLField( null = True, blank = True )
    date         = models.DateTimeField(default=datetime.now)
    status       = models.CharField( max_length = 255 )

    content_type = models.ForeignKey( ContentType, null = True, blank = True )
    object_id    = models.PositiveIntegerField( null = True, blank = True )
    object       = generic.GenericForeignKey()

    class Meta:
        verbose_name        = "исходящий"
        verbose_name_plural = "исходящие"
        db_table            = "turbion_pingback_outgoing"

dispatcher.connect( client.process_for_pingback, signal=signals.send_pingback )
