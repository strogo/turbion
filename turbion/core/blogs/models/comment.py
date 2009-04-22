from django.db import models, connection
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from turbion.core.profiles.models import Profile
from turbion.core.utils.markup.fields import MarkupTextField
from turbion.core.utils.models import GenericManager
from turbion.core.utils.enum import Enum
from turbion.core.blogs import signals as blogs_signals

class CommentManager(GenericManager):
    def get_query_set(self):
        return super(CommentManager, self).get_query_set().select_related("created_by")

class Comment(models.Model):
    post = models.ForeignKey('turbion.Post', related_name="comments", verbose_name=_("post"))

    statuses = Enum(
        published=_("published"),
        moderation=_("moderation"),
        hidden=_("hidden"),
        spam=_("spam"),
    )

    created_on = models.DateTimeField(default=datetime.now, verbose_name=_("created on"))

    created_by = models.ForeignKey(Profile, related_name="created_comments",
                                   verbose_name=_("created by"))

    edited_on = models.DateTimeField(null=True, editable=False, blank=True, verbose_name=_("edited on"))
    edited_by = models.ForeignKey(Profile, related_name="edited_comments",
                                  editable=False, null=True, verbose_name=_("edited by"))

    text = MarkupTextField(verbose_name=_("text"))

    status = models.CharField(max_length=20,
                              choices=statuses,
                              default=statuses.published,
                              verbose_name=_("status"))

    is_published = property(lambda self: self.status == Comment.statuses.published)

    objects = CommentManager()
    published = CommentManager(status=statuses.published)

    def is_edited(self):
        return self.created_on != self.edited_on

    def __unicode__(self):
        return _('Comment on %(post)s by %(author)s') % {'post': self.post, 'author': self.created_by.name,}

    def emit_event(self):
        from turbion.core import watchlist

        watchlist.emit_event(
            'new_comment',
            post=self.post,
            filter_recipient=lambda user: user != self.created_by,
            comment=self,
        )

    def subscribe_author(self, email=False):
        from turbion.core import watchlist

        watchlist.subscribe(
            'new_comment',
            self.created_by,
            post=self.post,
            email=email
        )

    def get_absolute_url(self):
        return self.post.get_absolute_url() + "#comment_%s" % self.pk

    def save(self, *args, **kwargs):
        if self.edited_by:
            self.edited_on = datetime.now()

        super(Comment, self).save(*args, **kwargs)

    class Meta:
        app_label           = "turbion"
        ordering            = ("-created_on",)
        verbose_name        = _('comment')
        verbose_name_plural = _('comments')
        db_table            = "turbion_comment"
