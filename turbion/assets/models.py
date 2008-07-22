# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType

from turbion.profiles.models import Profile

from pantheon.models import fields

class Asset(models.Model):
    name = models.CharField(max_length=250)
    filename = models.CharField(max_length=255)

    created_by = models.ForeignKey(Profile, related_name="assets")
    created_on = models.DateTimeField(default=datetime.now)

    edited_by = models.ForeignKey(Profile, null=True, related_name="edited_assets")
    edited_on = models.DateTimeField(null=True)

    description = models.TextField(null=True)
    mime_type = models.CharField(max_length=255)

    type = models.CharField(max_length=255)
    file = models.FileField(upload_to=settings.TURBION_BASE_UPLOAD_PATH + "assets/")

    def save( self ):
        if self.edited_by:
            self.edited_on = datetime.now()
        super( Asset, self ).save()

    class Meta:
        verbose_name        = _( "asset" )
        verbose_name_plural = _( "assets" )
        db_table            = "turbion_asset"

class Connection(models.Model):
    object_ct = models.ForeignKey(ContentType, related_name="assets_connections")
    object_id = models.PositiveIntegerField()

    asset = models.ForeignKey(Asset, related_name="connections")

    class Meta:
        unique_together = ["object_ct", "object_id", "asset"]
        db_table = "turbion_asset_connection"
