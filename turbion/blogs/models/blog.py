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

from turbion.socialbookmarks.models import Group
from turbion.comments.models import Comment
from turbion import roles

class Blog(models.Model):
    review_count = models.IntegerField( default = 0, editable = False, verbose_name = _( "review count" ) )

    slug = models.CharField(max_length = 50,
                            unique = True,
                            verbose_name=_("slug"))

    name = models.CharField(max_length=50,default ='Turbion Blog', verbose_name=_("name"))

    created_on = models.DateTimeField(default=datetime.now, editable=False, verbose_name=_("created on"))
    created_by = models.ForeignKey(Profile, related_name="created_blogs", verbose_name=_("created on"))

    post_per_page = models.SmallIntegerField(default=5, verbose_name=_("posts per page"))
    additional_post_fields = models.BooleanField(default=False)
    socialbookmarks_group = models.ForeignKey(Group, verbose_name=_("social bookmarks group"), null=True, blank=True)

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
            self._calendar = BlogCalendar(self,
                                          Post.published.for_blog(Blog.objects.get(pk=self._get_pk_val())))
        return self._calendar

    def inc_reviews(self):
        self.review_count += 1
        self.save()

    @utils.permalink
    def get_absolute_url(self):
        return ("blog_index", (self.slug,))

    @models.permalink
    def get_dashboard_url(self):
        return ("dashboard_blog_index", (self.slug,))

    @utils.permalink
    def get_atom_feed_url(self):
        return ("blog_atom", (self.slug, 'posts',))

    def per_page(self):
        return self.post_per_page

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
    date_field = "created_on"

    @models.permalink
    def get_month_url(self, date):
        return ("turbion.blogs.views.archive.month", (), {'year_id': date.year,
                                                     'month_id' : date.month,
                                                     'blog' :self.instance.slug})

    def get_per_day_urls(self, dates):
        from django.core.urlresolvers import reverse
        return dict([(date.date(), reverse("turbion.blogs.views.archive.day",
                                            kwargs = {'year_id': date.year,
                                                      'month_id': date.month,
                                                      'day_id': date.day,
                                                      'blog':self.instance.slug})) for date in dates])


class BlogRoles(roles.RoleSet):
    class Meta:
        model = Blog

    class Capabilities:
        enter_dashboard    = roles.Capability("Can enter blog dashboard")
        change_preferences = roles.Capability("Can change blog preferences")
        add_post           = roles.Capability("Can add new blog post")
        edit_post          = roles.Capability("Can edit blog post")
        delete_post        = roles.Capability("Can delete blog post")
        review_feedback    = roles.Capability("Can review blog feedback entries")
        edit_feedback      = roles.Capability("Can edit blog feedback entries")
        edit_comment       = roles.Capability("Can edit blog comments")
        upload_asset       = roles.Capability("Can upload blog asset")
        edit_asset         = roles.Capability("Can edit blog asset")
        add_page           = roles.Capability("Can add blog page")
        edit_page          = roles.Capability("Can edit blog page")
        delete_page        = roles.Capability("Can delete blog page")

    class Roles:
        blog_owner = roles.Role("Blog owner", ("enter_dashboard",
                                               "add_post",
                                               "edit_post",
                                               "delete_post",
                                               "change_preferences",
                                               "review_feedback",
                                               "edit_feedback",
                                               "edit_comment"))
