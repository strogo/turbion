# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.blogs.models import Blog
from turbion.notifications import EventDescriptor
from turbion.feedback import signals
from turbion.profiles.models import Profile

from turbion.utils.enum import Enum
from turbion.utils.models import GenericManager

class Feedback(models.Model):
    statuses = Enum(accepted=_("accepted"),
                    rejected=_("rejected"),
                    done    =_("done"),
                    new     =_("new"),
                )
    blog       = models.ForeignKey(Blog, related_name="feedbacks")

    created_on = models.DateTimeField(default=datetime.now, verbose_name=_('creation date'))
    created_by = models.ForeignKey(Profile, related_name="created_feedbacks")

    edited_on  = models.DateTimeField(verbose_name=_('update date'), null=True, blank=True)
    edited_by  = models.ForeignKey(Profile, related_name="edited_feedbacks", null=True, blank=True)

    subject    = models.CharField(max_length=255, verbose_name=_("subject"))

    text       = models.TextField(verbose_name=_('text'))

    status     = models.CharField(max_length=10, choices=statuses, default=statuses.new, verbose_name=_("status"))

    objects  = models.Manager()
    new      = GenericManager(status=statuses.new)
    accepted = GenericManager(status=statuses.accepted)

    def __unicode__(self):
        return "%s" % self.created_on

    def save(self, *args, **kwargs):
        if self.edited_by:
            self.edited_on = datetime.now()
        super(Feedback, self).save(*args, **kwargs)

    class Meta:
        verbose_name        = _('feedback')
        verbose_name_plural = _('feedbacks')
        ordering            = ('-created_on',)
        db_table            = "turbion_feedback"

class FeedbackAdd(EventDescriptor):
    class Meta:
        name = _("New feedback added")
        to_object = True
        trigger = (Feedback, signals.feedback_added)
