# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from turbion.blogs.models import Post, Comment

from django.utils.functional import curry
from django.db.models import signals
from django.conf import settings
from django.core.urlresolvers import reverse

class BlogSitemap(Sitemap):
    def __init__(self, blog):
        self.blog = blog

class PostSitemap(BlogSitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        query_set = Post.published.for_blog(self.blog)
        if not self.request.user.is_authenticated_confirmed():
            query_set = query_set.filter(showing=Post.show_settings.everybody)
        return query_set

    def lastmod(self, post):
        return post.edited_on

class CommentSitemap(BlogSitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Comment.published.for_object(self.blog)#FIXME: remove comments reg/private posts

    def lastmod(self, comment):
        return comment.date

class GlobalSitemap(Sitemap):
    pass
