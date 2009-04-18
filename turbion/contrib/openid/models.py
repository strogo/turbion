from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from turbion.core.utils.models import GenericManager
from turbion.core.utils.enum import Enum

# Models needed to openid library store

class Association(models.Model):
    origins = Enum(
        server=_("server"),
        consumer=_("consumer"),
    )
    server_url = models.TextField(max_length=2047)

    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.PositiveIntegerField()
    lifetime = models.PositiveIntegerField()
    assoc_type = models.CharField(max_length=64)

    origin = models.CharField(max_length=10, choices=origins, default=origins.consumer)

    def __unicode__(self):
        return self.handle

    class Meta:
        db_table = "turbion_openid_association"

class Nonce(models.Model):
    server_url = models.TextField(max_length=2047)
    timestamp = models.PositiveIntegerField()
    salt = models.CharField(max_length=40)

    origin = models.CharField(max_length=10, choices=Association.origins, default=Association.origins.consumer)

    def __unicode__(self):
        return "%s at %s" % (self.server_url, self.timestamp)

    class Meta:
        db_table = "turbion_openid_nonce"

# Public interface

class Trust(models.Model):
    url = models.URLField(unique=True, verbose_name=_('url'))
    date = models.DateTimeField(default=datetime.now, verbose_name=_('date'))

    def __unicode__(self):
        return self.url

    class Meta:
        db_table = "turbion_openid_trust"
        verbose_name = _('trust url')
        verbose_name_plural = _('trust urls')
