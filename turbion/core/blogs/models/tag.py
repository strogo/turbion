# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.models import GenericManager

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_("slug"))

    objects = models.Manager()
    active = GenericManager(posts=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.core.utils.text import slugify
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)


    class Meta:
        app_label           = "turbion"
        ordering            = ("name", "slug")
        verbose_name        = _("tag")
        verbose_name_plural = _("tags")
        db_table            = "turbion_tag"
