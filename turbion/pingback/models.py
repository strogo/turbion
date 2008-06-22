# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.dispatch import dispatcher
from turbion.pingback import client, signals

TYPE = ( ( 1, "pingback"),
         ( 2, "trackback" ))

class Incoming( models.Model ):
    source_url = models.URLField()
    target_url = models.CharField( max_length=255 )

    date = models.DateTimeField( default=datetime.now)
    status = models.CharField( max_length=255 )

    title = models.CharField( max_length=255, null = True )
    paragraph = models.TextField( null = True )

    content_type = models.ForeignKey( ContentType, null = True, blank = True )
    object_id = models.PositiveIntegerField( null = True, blank = True )
    object = generic.GenericForeignKey()

    class Admin:
        list_display= ( "target_url", "source_url", "date", "title", "status" )
        list_filter = ( "content_type", )
        list_per_page = 25

    class Meta:
        verbose_name = "входящий"
        verbose_name_plural = "входящие"
        unique_together = ( ( "source_url", "content_type", "object_id" ), )

class Outgoing( models.Model ):
    target_uri = models.URLField()
    title = models.CharField( max_length = 250 )
    rpcserver = models.URLField( null = True, blank = True )
    date = models.DateTimeField(default=datetime.now)
    status = models.CharField( max_length = 255 )

    content_type = models.ForeignKey( ContentType, null = True, blank = True )
    object_id = models.PositiveIntegerField( null = True, blank = True )
    object = generic.GenericForeignKey()

    class Meta:
        verbose_name = "исходящий"
        verbose_name_plural = "исходящие"


    class Admin:
        list_display = ( "target_uri", "date", "title", "status", "rpcserver", )
        list_filter = ( "content_type", )
        list_per_page = 25

dispatcher.connect( client.process_for_pingback, signal=signals.send_pingback )