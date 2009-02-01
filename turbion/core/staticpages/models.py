# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.postprocessing.fields import PostprocessedTextField
from turbion.core.utils.enum import Enum
from turbion.core.utils.models import GenericManager

from turbion.core.profiles.models import Profile

class Page(models.Model):
    statuses = Enum(
        published=_("published"),
        hide=_("hide")
    )

    created_on = models.DateTimeField(default=datetime.now,
                                      verbose_name=_('creation date'))
    created_by = models.ForeignKey(Profile, editable=False,
                                   related_name = "created_pages")

    edited_on  = models.DateTimeField(verbose_name=_('update date'),
                                      null=True, blank=True)
    edited_by  = models.ForeignKey(Profile, related_name="edited_pages", editable=False,
                                   null=True, blank=True)

    title      = models.CharField(max_length=100, verbose_name=_("title"))
    slug       = models.SlugField()

    text       = PostprocessedTextField(verbose_name=_("text"))

    status     = models.CharField(max_length=10, choices=statuses,
                                default=statuses.published, verbose_name=_("status"))

    template   = models.CharField(max_length=150, verbose_name=_("template"),
                                  null=True, blank=True)

    objects   = models.Manager()
    published = GenericManager(status=statuses.published)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.core.utils.text import slugify
            self.slug = slugify(self.title)

        if self.edited_by:
            self.edited_on = datetime.now()

        super(Page, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_pages_dispatcher", (self.slug,))

    class Meta:
        app_label           = "turbion"
        verbose_name        = _("page")
        verbose_name_plural = _("pages")
        db_table            = "turbion_page"
