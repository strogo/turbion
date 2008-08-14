# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class ConnectedModel(models.Model):
    connection_ct = models.ForeignKey(ContentType)
    connection_id = models.PositiveIntegerField()

    connection = GenericForeignKey("connection_ct", "connection_id")

    class Meta:
        abstract = True

class NullConnectedModel(models.Model):
    connection_ct = models.ForeignKey(ContentType, null=True)
    connection_id = models.PositiveIntegerField(null=True)

    connection = GenericForeignKey("connection_ct", "connection_id")

    class Meta:
        abstract = True

class GenericManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(GenericManager, self).__init__()
        self.args = args
        self.lookups = self.selectors = kwargs

    def get_query_set(self):
        return super(GenericManager, self).get_query_set().filter(*self.args, **self.selectors)
