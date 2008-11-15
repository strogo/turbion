# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.db import models

from turbion.utils.models import GenericManager

class GearInfo(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("name"))
    descriptor = models.CharField(max_length=250, unique=True, verbose_name=_("descriptor"))

    interval = models.CharField(max_length=250, verbose_name=_("interval"))

    last = models.DateTimeField(null=True, verbose_name=_("last"))
    next = models.DateTimeField(null=True, db_index=True, verbose_name=_("next"))

    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    is_lost = models.BooleanField(default=False, verbose_name=_("is lost"))

    objects = models.Manager()
    active = GenericManager(is_active=True, is_lost=False)

    def has_revolved(self):
        now = datetime.now()

        self.last = now

        interval = int(self.interval)

        self.next = now + timedelta(minutes=interval)

        self.save()

    def get_last_time(self):
        return self.next - timedelta(minutes=int(self.interval))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("gear info")
        verbose_name_plural = _("gear infos")
        db_table = "turbion_gear"
