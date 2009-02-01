# -*- coding: utf-8 -*-
from datetime import datetime
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from turbion.core.utils.descriptor import DescriptorField, GenericForeignKey, to_descriptor
from turbion.core.profiles.models import Profile
from turbion.core.utils.enum import Enum

class AssetManager(models.Manager):
    def for_object(self, obj):
        dscr = to_descriptor(obj.__class__)

        return self.filter(
                        connections__object_dscr=dscr,
                        connections__object_id=obj.pk
                )

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
        dscr = to_descriptor(obj.__class__)
        id = obj.pk

        AssetConnection.objects.get_or_create(
                    object_dscr=dscr,
                    object_id=id,
                    asset=self
                )

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
        app_label           = "turbion"
        verbose_name        = _("asset")
        verbose_name_plural = _("assets")
        db_table            = "turbion_asset"

class AssetConnection(models.Model):
    object_dscr = DescriptorField()
    object_id = models.PositiveIntegerField()
    object    = GenericForeignKey("object_dscr","object_id")

    asset = models.ForeignKey(Asset, related_name="connections")

    class Meta:
        app_label       = "turbion"
        unique_together = ["object_dscr", "object_id", "asset"]
        db_table        = "turbion_asset_connection"
