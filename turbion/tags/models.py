# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from pantheon.models import fields

from turbion.tags import managers

class Tag( models.Model ):
    name = models.CharField( max_length = 50, unique = True, verbose_name="Имя" )
    slug = fields.ExtSlugField( for_field = "name", editable = False,verbose_name="Слаг" )

    objects = managers.TagManager()

    def get_ratio( self, related_name, owner, all_count, object ):
        manager = getattr( self, related_name )
        count = manager.filter( **{ owner : object } ).count()
        return count / ( all_count + 1 )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ( "name", "slug" )
        verbose_name        = "tag"
        verbose_name_plural = "tags"

    class Admin:
        list_display = ( "name", "slug", )

class TaggedItem( models.Model ):
    tag = models.ForeignKey( Tag, related_name = "items" )

    item_ct = models.ForeignKey( ContentType )
    item_id = models.PositiveIntegerField()

    item = generic.GenericForeignKey( "item_ct", "item_id" )

    objects = managers.TaggedItemManager()

    class Meta:
        unique_together = ( ( "tag", "item_ct", "item_id" ), )
