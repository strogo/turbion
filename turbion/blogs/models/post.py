# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.blogs import managers
from turbion.blogs.models.blog import Blog
from turbion.comments.models import Comment
from turbion.comments.fields import CommentCountField
from turbion.tags.models import Tag
from turbion.tags.fields import TagsField
from turbion.profiles.models import Profile
from turbion.blogs import utils

from turbion.utils.postprocessing.fields import PostprocessedTextField
from turbion.utils.enum import Enum

class Post(models.Model):
    statuses = Enum(draft    =_("draft"),
                    trash    =_("trashed"),
                    published=_("published")
                )

    commenting_settings = Enum(allow   =_("allow"),
                               disallow=_("disallow"),
            )

    show_settings = Enum(everybody=_("everybody"),
                         registred=_("registered"),
            )

    blog          = models.ForeignKey(Blog, verbose_name=_("blog"), related_name="posts")
    comment_count = CommentCountField(verbose_name=_("comment count"))

    created_on    = models.DateTimeField(default=datetime.now, editable=False, verbose_name=_("created on"))
    created_by    = models.ForeignKey(Profile, related_name="created_posts", verbose_name=_("created by"))

    published_on  = models.DateTimeField(editable=False, verbose_name=_("published on"),
                                         blank=True, null=True, db_index=True)

    edited_on     = models.DateTimeField(null=True, editable=False, verbose_name=_("edited on"))
    edited_by     = models.ForeignKey(Profile, null=True, blank=True,
                                      related_name="edited_blogs", verbose_name=_("edited by"))

    title         = models.CharField(max_length=130, verbose_name=_("title"))
    slug          = models.CharField(max_length=130, editable=False,
                                     verbose_name=_("slug"), db_index=True)

    mood          = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("mood"))
    location      = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("location"))
    music         = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("music"))

    text          = PostprocessedTextField(verbose_name=_("text"))

    status        = models.CharField(max_length=10, choices=statuses, db_index=True,
                                     default=statuses.draft, verbose_name=_("status"))

    commenting    = models.CharField(max_length=10, choices=commenting_settings,
                                     default=commenting_settings.allow,
                                     verbose_name=_("commenting"))
    showing       = models.CharField(max_length = 10, choices=show_settings,
                                     default=show_settings.everybody,
                                     verbose_name=_("showing"),
                                     db_index=True)

    objects = managers.PostManager()

    published = managers.PostManager(status=statuses.published)

    tags = TagsField()

    @utils.permalink
    def get_absolute_url(self):
        args = (
            self.blog.slug, self.published_on.year, self.published_on.month,
            self.published_on.day, self.slug,
        )
        return ("turbion_blog_post", args)

    is_published = property(lambda self: self.status == Post.statuses.published)
    allow_comments = property(lambda self: self.commenting == Post.commenting_settings.allow)

    @models.permalink
    def get_atom_feed_url(self):
        return ("turbion_blog_atom", ("%s/%s" % (self.blog.slug, self.id),))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.utils.text import slugify
            self.slug = slugify(self.title)

        if self.edited_by:
            self.edited_on = datetime.now()

        super(Post, self).save(*args, **kwargs)

    def _get_near_post(self, is_next, **kwargs):
        if self.published_on is None:
            raise ValueError("Cannot find next or prev post when published_on is None")

        op = is_next and 'gt' or 'lt'
        order = not is_next and '-' or ''

        q = models.Q(**{'published_on__%s' % op: self.published_on})
        qs = self.__class__._default_manager.filter(**kwargs)\
                                        .filter(q)\
                                        .exclude(pk=self.pk)\
                                        .order_by('%spublished_on' % order)
        try:
            return qs[0]
        except IndexError:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    get_previous_by_published_on = lambda self, **kwargs: self._get_near_post(False, **kwargs)
    get_next_by_published_on = lambda self, **kwargs: self._get_near_post(True, **kwargs)

    class Meta:
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ('-published_on', '-created_on',)
        unique_together     = (("blog", "published_on", "title", "slug"),)
        app_label           = "blogs"
        db_table            = "turbion_post"
