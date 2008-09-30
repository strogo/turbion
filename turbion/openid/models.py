# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from turbion.profiles.models import Profile
from turbion.utils.models import GenericManager

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
    server_url = models.URLField(max_length=250)

    handle = models.CharField(max_length=250)
    secret = models.CharField(max_length=128)
    issued = models.PositiveIntegerField()
    lifetime = models.PositiveIntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        db_table = "turbion_openid_association"
        #unique_together = [('server_url', 'handle')]

class Nonce(models.Model):
    server_url = models.URLField()
    timestamp = models.PositiveIntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        db_table = "turbion_openid_nonce"
        unique_together = [('server_url', 'timestamp', 'salt')]

class Trust(models.Model):
    url = models.URLField(unique=True)
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "turbion_openid_trust"
