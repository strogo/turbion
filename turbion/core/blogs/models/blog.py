# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django import db
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.core.utils._calendar import Calendar
from turbion.core.utils.postprocessing.fields import PostprocessField
from turbion.core.utils import memoize
from turbion.core.blogs import managers
from turbion.core.tags.models import Tag
from turbion.core.profiles.models import Profile
from turbion.core.blogs import utils
from turbion.core.utils.enum import Enum
from turbion.core import capabilities

class Blog(models.Model):
    moderations = Enum(
        none=_("none"),
        all=_("all"),
        guests=_("guests"),
        untrusted=_("untrusted")
    )

    slug = models.CharField(
                    max_length=50,
                    unique=True,
                    verbose_name=_("slug")
            )

    name = models.CharField(max_length=50, default='Turbion Blog', verbose_name=_("name"))

    created_on = models.DateTimeField(default=datetime.now, editable=False, verbose_name=_("created on"))
    created_by = models.ForeignKey(Profile, related_name="created_blogs", verbose_name=_("created on"))

    post_per_page = models.SmallIntegerField(default=5, verbose_name=_("posts per page"))
    additional_post_fields = models.BooleanField(default=False)
    socialbookmarks = models.CharField(max_length=255, verbose_name=_("social bookmarks"), blank=True)
    comments_moderation = models.CharField(max_length=20, choices=moderations, default=moderations.none)

    objects = managers.BlogManager()

    def __unicode__(self):
        return self.name

    def get_post_count(self):
        from turbion.core.blogs.models.post import Post
        return Post.published.for_blog(self).count()

    @property
    def calendar(self):
        if not hasattr(self, "_calendar"):
            from turbion.core.blogs.models import Post
            self._calendar = BlogCalendar(
                self,
                Post.published.for_blog(self)
            )
        return self._calendar

    @utils.permalink
    def get_absolute_url(self):
        return ("turbion_blog_index", (self.slug,))

    @models.permalink
    def get_dashboard_url(self):
        return ("turbion_dashboard_blog_index", (self.slug,))

    @utils.permalink
    def get_atom_feed_url(self):
        return ("turbion_blog_atom", (self.slug, 'posts',))

    def per_page(self):
        return self.post_per_page

    def get_comment_status(self, comment):
        from turbion.core.comments.models import Comment

        author = comment.created_by

        if self.comments_moderation == Blog.moderations.all:
            return Comment.statuses.moderation

        elif self.comments_moderation == Blog.moderations.none:
            return Comment.statuses.published

        elif self.comments_moderation == Blog.moderations.guests:
            if not author.is_confirmed:
                return Comment.statuses.moderation

        elif self.comments_moderation == Blog.moderations.untrusted:
            if not author.is_confirmed or not author.trusted:
                return Comment.statuses.moderation

        return Comment.statuses.published

    @property
    def tags(self):
        from turbion.core.blogs.models.post import Post
        return Tag.objects.filter_for_model(Post, blog_id=self.id, **Post.published.lookups)

    @memoize
    def generate_menu(self):
        from turbion.core.staticpages.models import Page
        menu = [
            (_("blog"), self.get_absolute_url()),
            (_("feedback"), utils.reverse("turbion_feedback", args=(self.slug,))),
        ]

        menu += [(page.title, page.get_absolute_url())
                    for page in Page.published.filter(blog=self)]

        return menu

    class Meta:
        app_label           = "turbion"
        verbose_name        = _('blog')
        verbose_name_plural = _('blogs')
        db_table            = "turbion_blog"

class BlogCalendar(Calendar):
    date_field = "published_on"

    @utils.permalink
    def get_month_url(self, date):
        return "turbion_blog_archive_month", (self.instance.slug, date.year, date.month), {}

    def get_per_day_urls(self, dates):
        return dict([(date.date(), utils.reverse("turbion_blog_archive_day",
                                            args=(
                                                self.instance.slug,
                                                date.year,
                                                date.month,
                                                date.day
                                            )
                                        )) for date in dates])

class BlogCapabilities(capabilities.CapabilitySet):
    defs = dict(
        capabilities.generate_triple("post", "blog post") +
        capabilities.generate_triple("page", "blog static page")
#        review_feedback    = _("Can review blog feedback entries"),
#        edit_feedback      = _("Can edit blog feedback entries"),
#        edit_comment       = _("Can edit blog comments"),
#        upload_asset       = _("Can upload blog asset"),
#        edit_asset         = _("Can edit blog asset"),
    )

    def get_instance(self, instance):
        if isinstance(instance, Blog):
            return instance
        return instance.blog

capabilities.register(Blog, BlogCapabilities, name="blog.caps")
