from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils.models import GenericManager

class Template(models.Model):
    path = models.CharField(max_length=250, unique=True, verbose_name=_('path'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    text = models.TextField(verbose_name=_('text'))

    objects = models.Manager()
    active = GenericManager(is_active=True)

    def __unicode__(self):
        return self.path

    class Meta:
        verbose_name        = _("template")
        verbose_name_plural = _("templates")
        db_table            = "turbion_template"
