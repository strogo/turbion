# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.utils.descriptor import DescriptorField, GenericForeignKey
from turbion.tags import managers

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_("slug"))

    objects = managers.TagManager()

    def get_ratio(self, related_name, owner, all_count, object):
        manager = getattr(self, related_name)
        count = manager.filter(**{owner: object}).count()
        return count / (all_count + 1)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.utils.text import slugify
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)

    def connect(self, instance):
        item, _ = TaggedItem.objects.get_or_create_item(self, instance)

    class Meta:
        ordering            = ("name", "slug")
        verbose_name        = "tag"
        verbose_name_plural = "tags"
        db_table            = "turbion_tag"

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, related_name="items")

    item_dscr = DescriptorField()
    item_id = models.PositiveIntegerField()

    item = GenericForeignKey("item_dscr", "item_id")

    objects = managers.TaggedItemManager()

    class Meta:
        unique_together = [("tag", "item_dscr", "item_id"),]
        db_table        = "turbion_taggeditem"
