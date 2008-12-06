# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django import db
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.utils._calendar import Calendar
from turbion.utils.postprocessing.fields import PostprocessField

from turbion.blogs import managers
from turbion.tags.models import Tag
from turbion.profiles.models import Profile
from turbion.blogs import utils
from turbion.utils.enum import Enum

from turbion import roles

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
        from turbion.blogs.models.post import Post
        return Post.published.for_blog(self).count()

    @property
    def calendar(self):
        if not hasattr(self, "_calendar"):
            from turbion.blogs.models import Post
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
        from turbion.comments.models import Comment

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
        from turbion.blogs.models.post import Post
        return Tag.objects.filter_for_model(Post, blog_id=self.id, **Post.published.lookups)

    def is_author(self, user):
        return self.authors.filter(pk=user._get_pk_val()).count()

    class Meta:
        verbose_name        = _('blog')
        verbose_name_plural = _('blogs')
        app_label           = 'blogs'
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


class BlogRoles(roles.RoleSet):
    class Meta:
        model = Blog

    class Capabilities:
        enter_dashboard    = roles.Capability(_("Can enter blog dashboard"))
        change_preferences = roles.Capability(_("Can change blog preferences"))
        add_post           = roles.Capability(_("Can add new blog post"))
        edit_post          = roles.Capability(_("Can edit blog post"))
        delete_post        = roles.Capability(_("Can delete blog post"))
        review_feedback    = roles.Capability(_("Can review blog feedback entries"))
        edit_feedback      = roles.Capability(_("Can edit blog feedback entries"))
        edit_comment       = roles.Capability(_("Can edit blog comments"))
        upload_asset       = roles.Capability(_("Can upload blog asset"))
        edit_asset         = roles.Capability(_("Can edit blog asset"))
        add_page           = roles.Capability(_("Can add blog page"))
        edit_page          = roles.Capability(_("Can edit blog page"))
        delete_page        = roles.Capability(_("Can delete blog page"))

    class Roles:
        blog_owner = roles.Role("Blog owner", ("enter_dashboard",
                                               "add_post",
                                               "edit_post",
                                               "delete_post",
                                               "change_preferences",
                                               "review_feedback",
                                               "edit_feedback",
                                               "edit_comment"))
