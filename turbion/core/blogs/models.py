from datetime import datetime

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse

from turbion.core.blogs import managers
from turbion.core.profiles.models import Profile
from turbion.core.utils.markup.fields import MarkupTextField
from turbion.core.utils.enum import Enum

from turbion.core.utils._calendar import Calendar
from turbion.core.blogs.fields import PostCountField, CommentCountField
from turbion.core.utils.antispam import AntispamModel

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("name"))
    slug = models.CharField(max_length=50, unique=True, verbose_name=_("slug"))

    objects = models.Manager()
    active = managers.TagManager(post_count__gt=0)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_blog_tag", (self.slug,))

    def get_feed_url(self):
        return {
            "atom": reverse("turbion_blog_atom", args=("tag/%s" % self.pk,)),
            "rss": reverse("turbion_blog_rss", args=("tag/%s" % self.pk,))
        }

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.core.utils.text import slugify
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)

    class Meta:
        app_label           = "turbion"
        ordering            = ("name", "slug")
        verbose_name        = _("tag")
        verbose_name_plural = _("tags")
        db_table            = "turbion_tag"

class Post(models.Model):
    moderations = Enum(
        none=_("none"),
        all=_("all"),
        untrusted=_("untrusted")
    )

    statuses = Enum(
        draft=_("draft"),
        trash=_("trashed"),
        hidden=_("hidden"),
        published=_("published")
    )

    commenting_settings = Enum(
        allow =_("allow"),
        disallow=_("disallow"),
    )

    show_settings = Enum(
        everybody=_("everybody"),
        registred=_("registered"),
    )

    created_on    = models.DateTimeField(default=datetime.now, editable=False, verbose_name=_("created on"))
    created_by    = models.ForeignKey(Profile, related_name="created_posts", verbose_name=_("created by"))

    published_on  = models.DateTimeField(editable=False, verbose_name=_("published on"),
                                         blank=True, null=True, db_index=True)

    edited_on     = models.DateTimeField(null=True, editable=False, verbose_name=_("edited on"))
    edited_by     = models.ForeignKey(Profile, null=True, blank=True,
                                      related_name="edited_blogs", verbose_name=_("edited by"))

    title         = models.CharField(max_length=130, verbose_name=_("title"))
    slug          = models.CharField(max_length=130, verbose_name=_("slug"), blank=True, db_index=True)

    text          = MarkupTextField(verbose_name=_("text"))

    status        = models.CharField(max_length=10, choices=statuses, db_index=True,
                                     default=statuses.draft, verbose_name=_("status"))

    commenting    = models.CharField(max_length=10, choices=commenting_settings,
                                     default=commenting_settings.allow,
                                     verbose_name=_("commenting"))
    showing       = models.CharField(max_length = 10, choices=show_settings,
                                     default=show_settings.everybody,
                                     verbose_name=_("showing"),
                                     db_index=True)
    comments_moderation =  models.CharField(max_length=20, choices=moderations,
                                            default=moderations.none,
                                            verbose_name=_("comments moderation"))

    tags = models.ManyToManyField("turbion.Tag", related_name="posts", blank=True)

    objects = managers.PostManager()

    published = managers.PostManager(status=statuses.published)

    @models.permalink
    def get_absolute_url(self):
        if self.is_published:
            args = (
                self.published_on.year, '%02d' % self.published_on.month,
                '%02d' % self.published_on.day, self.slug,
            )
            return ('turbion_blog_post', args)
        else:
            return ('turbion_blog_post_preview', (self.pk,))

    is_published = property(lambda self: self.status == Post.statuses.published)
    allow_comments = property(lambda self: self.commenting == Post.commenting_settings.allow)

    def get_feed_url(self):
        return {
            "atom": reverse("turbion_blog_atom", args=("comments/%s" % self.pk,)),
            "rss": reverse("turbion_blog_rss", args=("comments/%s" % self.pk,))
        }

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.core.utils.text import slugify
            self.slug = slugify(self.title)

        self.edited_on = datetime.now()

        super(Post, self).save(*args, **kwargs)

    def publicate(self):
        from turbion.core.blogs import signals
        from turbion.core import watchlist

        self.published_on = datetime.now()

        self.save()

        watchlist.subscribe(self.created_by, 'new_comment', self, True)

        signals.post_published.send(
            sender=self.__class__,
            post=self
        )

    def _get_near_post(self, is_next, **kwargs):
        if self.published_on is None:
            raise ValueError("Cannot find next or prev post when published_on is None")

        op = is_next and 'gt' or 'lt'
        order = not is_next and '-' or ''

        kwargs.update({
            'published_on__%s' % op: self.published_on,
            'published_on__isnull': False
        })
        qs = self.__class__._default_manager.filter(**kwargs).exclude(pk=self.pk)\
                                        .order_by('%spublished_on' % order)
        try:
            return qs[0]
        except IndexError:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    get_previous_by_published_on = lambda self, **kwargs: self._get_near_post(False, **kwargs)
    get_next_by_published_on = lambda self, **kwargs: self._get_near_post(True, **kwargs)

    def get_comment_status(self, comment):
        author = comment.created_by

        if self.comments_moderation == Post.moderations.all:
            return Comment.statuses.moderation

        elif self.comments_moderation == Post.moderations.none:
            return Comment.statuses.published

        elif self.comments_moderation == Post.moderations.untrusted:
            if not author.is_trusted():
                return Comment.statuses.moderation

        return Comment.statuses.published

    def allow_comment_from(self, profile):
        return self.commenting == Post.commenting_settings.allow

    class Meta:
        app_label           = "turbion"
        verbose_name        = _('post')
        verbose_name_plural = _('posts')
        ordering            = ('-published_on', '-created_on',)
        unique_together     = (("published_on", "title", "slug"),)
        db_table            = "turbion_post"

Tag.add_to_class('post_count', PostCountField(verbose_name=_("post count")))

class Comment(models.Model, AntispamModel):
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

    objects = managers.CommentManager()
    published = managers.CommentManager(status=statuses.published)

    def is_edited(self):
        return self.created_on != self.edited_on

    def __unicode__(self):
        return _('Comment on %(post)s by %(author)s') % {'post': self.post, 'author': self.created_by.name,}

    def emit_event(self):
        from turbion.core import watchlist

        if not self.is_published:
            return

        watchlist.emit_event(
            'new_comment',
            post=self.post,
            filter_recipient=lambda user: user.email != self.created_by.email,
            comment=self,
        )

    def subscribe_author(self, email=False):
        from turbion.core import watchlist

        watchlist.subscribe(
            self.created_by,
            'new_comment',
            post=self.post,
            email=email
        )

    def get_absolute_url(self):
        return self.post.get_absolute_url() + "#comment_%s" % self.pk

    def save(self, *args, **kwargs):
        if self.edited_by:
            self.edited_on = datetime.now()

        super(Comment, self).save(*args, **kwargs)

    # some antispam methods
    def get_antispam_data(self):
        return {
            'permalink': self.post.get_absolute_url(),
            'comment_type': 'comment',
            'comment_author': self.created_by.name,
            'comment_author_email': self.created_by.email,
            'comment_author_url': self.created_by.site or self.created_by.openid,
            'comment_content': self.text,
            'user_ip': self.created_by.ip,
        }

    def get_antispam_status(self):
        return self.status

    def get_antispam_action(self):
        return self.status == Comment.status.published and 'spam' or 'ham'

    def set_antispam_status(self, decision):
        decision_map = {
            'ham': Comment.statuses.published,
            'spam': Comment.statuses.spam,
            'unknown': Comment.statuses.moderation
        }
        self.status = decision_map.get(decision, Comment.statuses.moderation)

    class Meta:
        app_label           = "turbion"
        ordering            = ("-created_on",)
        verbose_name        = _('comment')
        verbose_name_plural = _('comments')
        db_table            = "turbion_comment"

Post.add_to_class('comment_count', CommentCountField(verbose_name=_("comment count")))

class BlogCalendar(Calendar):
    date_field = "published_on"
    queryset = Post.published.all()

    @models.permalink
    def get_month_url(self, date):
        return "turbion_blog_archive_month", (date.year, date.month), {}

    def get_per_day_urls(self, dates):
        return dict(
            [
                (
                    date.date(),
                    reverse(
                        "turbion_blog_archive_day",
                        args=(
                            date.year,
                            date.month,
                            date.day
                        )
                    )
                ) for date in dates
            ]
        )
