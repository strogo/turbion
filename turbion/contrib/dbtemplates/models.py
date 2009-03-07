from django.db import models

from turbion.core.utils.models import GenericManager

class Template(models.Model):
    path = models.CharField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField()

    objects = models.Manager()
    active = GenericManager(is_active=True)

    def __unicode__(self):
        return self.path

    class Meta:
        verbose_name        = "template"
        verbose_name_plural = "templates"
        db_table            = "turbion_template"
