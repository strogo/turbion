# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from turbion.profiles.models import Profile
from turbion.utils.models import GenericManager
from turbion.utils.enum import Enum

class IdentityManager(GenericManager):
    def add_identifier(self, username, openid_url, **kwargs):
        user = User.objects.get(username=username)

        identity, _ = self.get_or_create(user=user, url=openid_url, defaults=kwargs)

        return identity

class Identity(models.Model):
    user = models.ForeignKey(Profile, null=True, related_name="openid_identifiers")

    date = models.DateTimeField(default=datetime.now)

    last_login = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=250, unique=True)
    default = models.BooleanField(default=False)
    local = models.BooleanField(default=False)

    objects = IdentityManager()
    locals = IdentityManager(local=True)
    globals = IdentityManager(local=False)

    class Meta:
        db_table = "turbion_openid_identity"

# models needed to openid library store

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
        #unique_together = [('server_url', 'handle')]

class Nonce(models.Model):
    server_url = models.TextField(max_length=2047)
    timestamp = models.PositiveIntegerField()
    salt = models.CharField(max_length=40)

    origin = models.CharField(max_length=10, choices=Association.origins, default=Association.origins.consumer)

    def __unicode__(self):
        return "%s at %s" % (self.server_url, self.timestamp)

    class Meta:
        db_table = "turbion_openid_nonce"
        #unique_together = [('server_url', 'timestamp', 'salt')]

class Trust(models.Model):
    url = models.URLField(unique=True)
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "turbion_openid_trust"
