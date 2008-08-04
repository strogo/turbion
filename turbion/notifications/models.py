# -*- coding: utf-8 -*-
from django.db import models
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from turbion.profiles.models import Profile

class EventManager(models.Manager):
    pass

class Event(models.Model):
    descriptor = models.CharField(max_length=250, unique=True)

    template = models.CharField(max_length=250, null=True, blank=True)
    subject_title = models.CharField(max_length=250)

    def __unicode__(self):
        return self.descriptor

    class Meta:
        verbose_name        = _("event")
        verbose_name_plural = _("events")
        db_table            = "turbion_event"

class Connection(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Profile, related_name="notification_recipient")

    connection_ct = models.ForeignKey(ContentType, null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_ct", "connection_id")

    def __unicode__(self):
        return "%s: %s-%s" % (self.event, self.connection_ct, self.connection_id)

    class Meta:
        verbose_name        = _("event connection")
        verbose_name_plural = _("event connections")
        unique_together     = [("event", "user", "connection_ct", "connection_id")]
        db_table            = "turbion_event_connection"
