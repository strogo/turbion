# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from turbion.profiles.models import Profile

class IdentityManager(models.Manager):
    def add_identifier(self, username, openid_url):
        user = User.objects.get(username=username)

        identity, _ = self.get_or_create(user=user, url=openid_url)

        return identity

class Identity(models.Model):
    user = models.ForeignKey(Profile, null=True, related_name="openid_identifiers")

    date = models.DateTimeField(default=datetime.now)

    last_login = models.DateTimeField(null=True, blank=True)
    url = models.URLField(max_length=250, unique=True )

    objects = IdentityManager()

    class Meta:
        db_table = "turbion_openid_identity"

# models needed to openid library store interface

class Association(models.Model):
    server_url = models.URLField()

    handle = models.CharField(max_length=240)
    secret = models.CharField(max_length=250)
    issued = models.PositiveIntegerField()
    lifetime = models.PositiveIntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        db_table = "turbion_openid_association"
        unique_together = [('server_url', 'handle')]

class Nonce(models.Model):
    server_url = models.URLField()
    timestamp = models.PositiveIntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        db_table = "turbion_openid_nonce"
        unique_together = [('server_url', 'timestamp', 'salt')]
