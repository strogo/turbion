# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.blogs import managers
from turbion.blogs.models.blog import Blog
from turbion.comments.models import Comment, CommentedModel
from turbion.tags.models import Tag
from turbion.tags.fields import TagsField
from turbion.profiles.models import Profile
from turbion.blogs import utils

from turbion.utils.postprocessing.fields import PostprocessField
from turbion.utils.enum import Enum

class Post(models.Model, CommentedModel):
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
    comment_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("comment count"))

    created_on    = models.DateTimeField(default=datetime.now, editable=False, verbose_name=_("created on"))
    created_by    = models.ForeignKey(Profile, related_name="created_posts", verbose_name=_("created by"))

    published_on  = models.DateTimeField(editable=False, verbose_name=_("published on"), blank=True, null=True, db_index=True)

    edited_on     = models.DateTimeField(null=True, editable=False, verbose_name=_("edited on"))
    edited_by     = models.ForeignKey(Profile, null=True, blank=True, related_name="edited_blogs", verbose_name=_("edited by"))

    review_count  = models.IntegerField(default=0, editable=False, verbose_name=_("review count"))

    title         = models.CharField(max_length=130, verbose_name=_("title"))
    slug          = models.CharField(max_length=130, editable=False, verbose_name=_("slug"), db_index=True)

    mood          = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("mood"))
    location      = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("location"))
    music         = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("music"))

    text          = models.TextField(verbose_name=_("text"))
    text_html     = models.TextField(verbose_name=_("text html"))

    status        = models.CharField(max_length=10, choices=statuses, default=statuses.draft, verbose_name=_("status"))

    postprocessor = PostprocessField(verbose_name=_("postprocessor"))

    commenting    = models.CharField(max_length=10,
                                     choices = commenting_settings,
                                     default = commenting_settings.allow,
                                     verbose_name=_("commenting"))
    showing       = models.CharField(max_length = 10,
                                     choices = show_settings,
                                     default = show_settings.everybody,
                                     verbose_name=_("showing"))

    objects = managers.PostManager()

    published = managers.PostManager(status=statuses.published)

    tags = TagsField()

    @utils.permalink
    def get_absolute_url(self):
        return ("turbion.blogs.views.post.post", (), { "year_id"   : self.created_on.year,
                                                        "month_id"  : self.created_on.month,
                                                        "day_id"    : self.created_on.day,
                                                        "post_slug" : self.slug,
                                                        "blog"      : self.blog.slug})

    is_published = property(lambda self: self.status == Post.statuses.published)
    allow_comments = property(lambda self: self.commenting == Post.commenting_settings.allow)

    @models.permalink
    def get_atom_feed_url(self):
        return ("blog_atom", ("%s/%s" % (self.blog.slug, self.id),))

    def inc_reviews(self):
        self.__class__._default_manager.\
                    filter(pk=self._get_pk_val()).\
                    update(review_count=self.review_count + 1)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from turbion.utils.text import slugify
            self.slug = slugify(self.title)
        if self.edited_by:
            self.edited_on = datetime.now()

        self.text_html = self.postprocessor.postprocess(self.text)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name        = 'post'
        verbose_name_plural = 'posts'
        ordering            = ('-published_on', '-created_on',)
        unique_together     = (("blog", "published_on", "title", "slug"),)
        app_label           = "blogs"
        db_table            = "turbion_post"
