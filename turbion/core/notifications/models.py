from datetime import datetime

from django.db import models
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

from turbion.core.profiles.models import Profile
from turbion.core.utils.descriptor import DescriptorField, GenericForeignKey

class EventManager(models.Manager):
    pass

class Event(models.Model):
    descriptor = DescriptorField(max_length=250, unique=True)

    template = models.CharField(max_length=250, null=True, blank=True)
    subject_title = models.CharField(max_length=250)

    def __unicode__(self):
        return self.descriptor

    class Meta:
        app_label           = "turbion"
        verbose_name        = _("event")
        verbose_name_plural = _("events")
        db_table            = "turbion_event"

class EventConnection(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(Profile, related_name="notification_recipient")

    connection_dscr = DescriptorField(null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_dscr", "connection_id")

    def __unicode__(self):
        return "%s: %s-%s" % (self.event, self.connection_dscr, self.connection_id)

    class Meta:
        app_label           = "turbion"
        verbose_name        = _("event connection")
        verbose_name_plural = _("event connections")
        unique_together     = [("event", "user", "connection_dscr", "connection_id")]
        db_table            = "turbion_event_connection"

class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)

    body = models.TextField()
    content_type = models.CharField(max_length=50, blank=True)

    def send(self):
        domain = Site.objects.get_current().domain
        from_email = settings.TURBION_NOTIFACTIONS_FROM_EMAIL % {"domain": domain}

        msg = EmailMessage(
            self.subject,
            self.body,
            from_email,
            [self.email]
        )

        if self.content_type:
            msg.content_subtype = self.content_type

        msg.send()

    class Meta:
        ordering = ['date']
        app_label = "turbion"
