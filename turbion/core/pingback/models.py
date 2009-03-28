from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models

from turbion.core.blogs import signals
from turbion.core.pingback import client
from turbion.core.utils.enum import Enum
from turbion.core.utils.models import GenericManager

from turbion.core.blogs.models import Post

class Pingback(models.Model):
    incoming   = models.BooleanField(verbose_name=_("incoming"))

    source_url = models.URLField(max_length=500,verbose_name=_("source url"))
    target_url = models.CharField(max_length=500, verbose_name=_("target url"))

    date       = models.DateTimeField(default=datetime.now, verbose_name=_("date"))
    status     = models.CharField(max_length=500, verbose_name=_("status"))
    finished   = models.BooleanField(default=False, verbose_name=_("finished"))

    title      = models.CharField(max_length=500, null=True, verbose_name=_("title"))
    paragraph  = models.TextField(null=True, verbose_name=_("paragraph"))

    post       = models.ForeignKey(Post, verbose_name=_("post"))

    objects = models.Manager()

    incomings = GenericManager(incoming=True, finished=True)
    outgoings = GenericManager(incoming=False, finished=True)

    class Meta:
        app_label           = "turbion"
        verbose_name        = _("pingback")
        verbose_name_plural = _("pingbacks")
        db_table            = "turbion_pingback"
        ordering            = ["-date", "-finished"]

signals.post_published.connect(client.process_for_pingback)
