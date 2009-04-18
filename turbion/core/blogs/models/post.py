from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from turbion.core.blogs import managers
from turbion.core.blogs.fields import CommentCountField
#from turbion.core.blogs.models.tag import Tag
from turbion.core.profiles.models import Profile
from turbion.core.utils.markup.fields import MarkupTextField
from turbion.core.utils.enum import Enum

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

    objects = managers.PostManager()

    published = managers.PostManager(status=statuses.published)

    tags = models.ManyToManyField("turbion.Tag", related_name="posts", blank=True)

    @models.permalink
    def get_absolute_url(self):
        args = (
            self.published_on.year, self.published_on.month,
            self.published_on.day, self.slug,
        )
        return ("turbion_blog_post", args)

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
        from turbion.core.blogs.models.comment import CommentAdd
        from turbion.core.blogs import signals

        self.published_on = datetime.now()

        self.save()

        CommentAdd.manager.subscribe(self.created_by, self)

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
        from turbion.core.blogs.models.comment import Comment

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
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ('-published_on', '-created_on',)
        unique_together     = (("published_on", "title", "slug"),)
        db_table            = "turbion_post"

Post.add_to_class("comment_count", CommentCountField(verbose_name=_("comment count")))
