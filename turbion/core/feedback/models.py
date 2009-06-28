from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from turbion.core.feedback import signals
from turbion.core.profiles.models import Profile
from turbion.core.utils.enum import Enum
from turbion.core.utils.models import FilteredManager

class Feedback(models.Model):
    statuses = Enum(
        accepted=_("accepted"),
        rejected=_("rejected"),
        done=_("done"),
        new=_("new"),
    )

    created_on = models.DateTimeField(default=datetime.now, editable=False,
                                      verbose_name=_('creation on'))
    created_by = models.ForeignKey(Profile, related_name="created_feedbacks",
                                   verbose_name=_("created by"))

    edited_on  = models.DateTimeField(verbose_name=_('update on'), editable=False,
                                      null=True, blank=True)
    edited_by  = models.ForeignKey(Profile, related_name="edited_feedbacks", editable=False,
                                   verbose_name=_("edited by"), null=True, blank=True)

    subject    = models.CharField(max_length=255, verbose_name=_("subject"))

    text       = models.TextField(verbose_name=_('text'))

    status     = models.CharField(max_length=10, choices=statuses,
                                  default=statuses.new, verbose_name=_("status"))

    objects  = models.Manager()
    new      = FilteredManager(status=statuses.new)
    accepted = FilteredManager(status=statuses.accepted)

    def __unicode__(self):
        return "%s by %s" % (self.subject, self.created_by)

    def save(self, *args, **kwargs):
        if self.edited_by:
            self.edited_on = datetime.now()
        super(Feedback, self).save(*args, **kwargs)

    # some antispam methods
    def get_antispam_data(self):
        return {
            'permalink': reverse('turbion_feedback'),
            'comment_type': 'feedback',
            'comment_author': self.created_by.name,
            'comment_author_email': self.created_by.email,
            'comment_author_url': self.created_by.site or self.created_by.openid,
            'comment_content': self.text,
            'user_ip': self.created_by.ip,
        }

    def get_antispam_status(self):
        if self.status.startswith('spam'):
            return self.status

        return 'ham'

    def set_antispam_status(self, decision):
        decision_map = {
            'ham': Comment.statuses.published,
            'spam': Comment.statuses.spam,
            'unknown': Comment.statuses.moderation
        }
        self.status = decision_map.get(decision, Comment.statuses.moderation)

    class Meta:
        verbose_name        = _('feedback')
        verbose_name_plural = _('feedbacks')
        ordering            = ('-created_on',)
        db_table            = "turbion_feedback"
