# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from turbion.pingback import client, signals

from turbion.utils.enum import Enum
from turbion.utils.descriptor import DescriptorField, GenericForeignKey

class Incoming(models.Model):
    types = Enum( pingback  = "pingback",
                  trackback = "trackback" )

    type         = models.CharField(max_length=10, choices=types, default=types.pingback)

    source_url   = models.URLField()
    target_url   = models.CharField( max_length=255 )

    date         = models.DateTimeField( default=datetime.now)
    status       = models.CharField( max_length=255 )

    title        = models.CharField( max_length=255, null = True )
    paragraph    = models.TextField( null = True )

    descriptor = DescriptorField(null=True, blank=True)
    object_id    = models.PositiveIntegerField(null=True, blank=True)
    object       = generic.GenericForeignKey()

    class Meta:
        verbose_name        = "входящий"
        verbose_name_plural = "входящие"
        unique_together     = (("source_url", "descriptor", "object_id"),)
        db_table            = "turbion_pingback_incoming"

class Outgoing(models.Model):
    target_uri   = models.URLField()
    title        = models.CharField( max_length = 250 )
    rpcserver    = models.URLField( null = True, blank = True )
    date         = models.DateTimeField(default=datetime.now)
    status       = models.CharField( max_length = 255 )

    descriptor = DescriptorField(null=True, blank=True)
    object_id    = models.PositiveIntegerField(null=True, blank=True)
    object       = generic.GenericForeignKey()

    class Meta:
        verbose_name        = "исходящий"
        verbose_name_plural = "исходящие"
        db_table            = "turbion_pingback_outgoing"

signals.send_pingback.connect(client.process_for_pingback)
