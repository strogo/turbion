# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from turbion.tags import managers

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_("slug"))

    objects = managers.TagManager()

    def get_ratio(self, related_name, owner, all_count, object):
        manager = getattr( self, related_name )
        count = manager.filter( **{ owner : object } ).count()
        return count / ( all_count + 1 )

    def __unicode__(self):
        return self.name

    def save(self):
        if not self.slug:
            from turbion.utils.text import slugify
            self.slug = slugify(self.title)

        super(Tag, self).save()

    class Meta:
        ordering            = ("name", "slug")
        verbose_name        = "tag"
        verbose_name_plural = "tags"
        db_table            = "turbion_tag"

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, related_name="items")

    item_ct = models.ForeignKey(ContentType)
    item_id = models.PositiveIntegerField()

    item = generic.GenericForeignKey("item_ct", "item_id")

    objects = managers.TaggedItemManager()

    class Meta:
        unique_together = [("tag", "item_ct", "item_id"),]
        db_table        = "turbion_taggeditem"
