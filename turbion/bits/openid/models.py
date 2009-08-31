from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from datetime import datetime

from turbion.bits.utils.models import FilteredManager
from turbion.bits.utils.enum import Enum

class Trust(models.Model):
    url = models.URLField(unique=True, verbose_name=_('url'))
    date = models.DateTimeField(default=datetime.now, verbose_name=_('date'))

    def __unicode__(self):
        return self.url

    class Meta:
        app_label = 'turbion'
        db_table = "turbion_openid_trust"
        verbose_name = _('trust url')
        verbose_name_plural = _('trust urls')
