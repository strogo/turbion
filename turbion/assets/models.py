# -*- coding: utf-8 -*-
from datetime import datetime
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from turbion.profiles.models import Profile
from turbion.utils.enum import Enum

class AssetManager(models.Manager):
    def for_object(self, obj):
        ct = ContentType.objects.get_for_model(obj.__class__)

        return self.filter(connections__object_ct=ct, connections__object_id=obj._get_pk_val())

class Asset(models.Model):
    types = Enum(image = _("image"),
                 application = _("application"),
                 video = _("video"),
                 audio = _("audio"),
                 unknown = _("unknown")
                )

    name = models.CharField(max_length=250)
    filename = models.CharField(max_length=255)

    created_by = models.ForeignKey(Profile, related_name="assets")
    created_on = models.DateTimeField(default=datetime.now)

    edited_by = models.ForeignKey(Profile, null=True, related_name="edited_assets")
    edited_on = models.DateTimeField(null=True)

    description = models.TextField(null=True, blank=True)
    mime_type = models.CharField(max_length=255)

    type = models.CharField(max_length=255, choices=types)
    file = models.FileField(upload_to=settings.TURBION_BASE_UPLOAD_PATH + "assets/")

    objects = AssetManager()

    def __unicode__(self):
        return self.name

    def get_thumbnail_url(self):
        filename = self.get_file_filename()
        dirname = os.path.dirname(filename)
        bits = os.path.splitext(os.path.basename(filename))
        return os.path.join(dirname, bits[0] + "_thumb" + bits[1])

    def connect_to(self, obj):
        ct = ContentType.objects.get_for_model(obj.__class__)
        id = obj._get_pk_val()

        Connection.objects.get_or_create(object_ct=ct, object_id=id, asset=self)

    def save(self, *args, **kwargs):
        if self.edited_by:
            self.edited_on = datetime.now()
        super(Asset, self).save(*args, **kwargs)

    def delete(self):
        super(Asset,self).delete()

        try:
            os.remove(self.get_thumbnail_url())
        except OSError:
            pass

    class Meta:
        verbose_name        = _("asset")
        verbose_name_plural = _("assets")
        db_table            = "turbion_asset"

class Connection(models.Model):
    object_ct = models.ForeignKey(ContentType, related_name="assets_connections")
    object_id = models.PositiveIntegerField()
    object    = generic.GenericForeignKey("object_ct","object_id")

    asset = models.ForeignKey(Asset, related_name="connections")

    class Meta:
        unique_together = ["object_ct", "object_id", "asset"]
        db_table = "turbion_asset_connection"
