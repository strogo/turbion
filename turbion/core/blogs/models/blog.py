# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django import db
from django.utils.translation import ugettext_lazy as _
from django.db import models

from turbion.core.utils._calendar import Calendar
from turbion.core.blogs.models import Post
from turbion.core import capabilities

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

#capabilities.register(Blog, BlogCapabilities, name="blog.caps")
