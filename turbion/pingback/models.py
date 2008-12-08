# -*- coding: utf-8 -*-
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models

from turbion.pingback import client, signals
from turbion.utils.enum import Enum
from turbion.utils.models import GenericManager
from turbion.utils.descriptor import DescriptorField, GenericForeignKey

class IncomingManager(GenericManager):
    def for_object(self, obj):
        from turbion.utils.descriptor import to_descriptor

        return self.filter(
            descriptor=to_descriptor(obj.__class__),
            object_id=obj._get_pk_val()
        )

class Incoming(models.Model):
    types = Enum(
        pingback="pingback",
        trackback="trackback"
    )

    type       = models.CharField(max_length=10, choices=types, default=types.pingback,
                                  verbose_name=_("type"))

    source_url = models.URLField(verbose_name=_("source url"))
    target_url = models.CharField(max_length=255, verbose_name=_("target url"))

    date       = models.DateTimeField(default=datetime.now, verbose_name=_("date"))
    status     = models.CharField(max_length=255, verbose_name=_("status"))
    finished   = models.BooleanField(default=False, verbose_name=_("finished"))

    title      = models.CharField(max_length=255, null=True, verbose_name=_("title"))
    paragraph  = models.TextField(null=True, verbose_name=_("paragraph"))

    descriptor = DescriptorField(null=True, blank=True, verbose_name=_("descriptor"))
    object_id  = models.PositiveIntegerField(null=True, blank=True)
    object     = GenericForeignKey()

    objects = models.Manager()
    pingbacks = IncomingManager(type=types.pingback, finished=True)
    trackbacks = IncomingManager(type=types.trackback, finished=True)

    class Meta:
        verbose_name        = _("incoming")
        verbose_name_plural = _("incomings")
        unique_together     = (("source_url", "descriptor", "object_id"),)
        db_table            = "turbion_pingback_incoming"

class Outgoing(models.Model):
    target_uri   = models.URLField(verbose_name=_("target uri"))
    title        = models.CharField(max_length=250, verbose_name=_("title"))
    rpcserver    = models.URLField(null=True, blank=True, verbose_name=_("rpc server"))
    date         = models.DateTimeField(default=datetime.now, verbose_name=_("date"))
    status       = models.CharField(max_length=255, verbose_name=_("status"))

    descriptor   = DescriptorField(null=True, blank=True, verbose_name=_("descriptor"))
    object_id    = models.PositiveIntegerField(null=True, blank=True)
    object       = GenericForeignKey()

    class Meta:
        verbose_name        = _("outgoing")
        verbose_name_plural = _("outgoings")
        db_table            = "turbion_pingback_outgoing"

signals.send_pingback.connect(client.process_for_pingback)
