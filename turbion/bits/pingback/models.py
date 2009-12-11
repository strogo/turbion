from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save

from turbion.bits.pingback import client
from turbion.bits.utils.models import FilteredManager

from turbion.bits.blogs.models import Post, Comment

class Pingback(models.Model):
    incoming   = models.BooleanField(verbose_name=_("incoming"))

    source_url = models.URLField(max_length=500, verify_exist=False, verbose_name=_("source url"))
    target_url = models.CharField(max_length=500, verify_exist=False, verbose_name=_("target url"))

    date       = models.DateTimeField(default=datetime.now, verbose_name=_("date"))
    status     = models.CharField(max_length=500, verbose_name=_("status"))
    finished   = models.BooleanField(default=False, verbose_name=_("finished"))

    title      = models.CharField(max_length=500, null=True, verbose_name=_("title"))
    paragraph  = models.TextField(null=True, verbose_name=_("paragraph"))

    post       = models.ForeignKey(Post, verbose_name=_("post"), null=True, blank=True)

    objects   = models.Manager()
    incomings = FilteredManager(incoming=True, finished=True)
    outgoings = FilteredManager(incoming=False, finished=True)

    class Meta:
        app_label           = "turbion"
        verbose_name        = _("pingback")
        verbose_name_plural = _("pingbacks")
        db_table            = "turbion_pingback"
        ordering            = ["-date", "-finished"]


def handle_published(instance, *args, **kwargs):
    if instance.is_published:
        return client.ping_links(instance=instance, *args, **kwargs)

post_save.connect(handle_published, sender=Post)
post_save.connect(handle_published, sender=Comment)
