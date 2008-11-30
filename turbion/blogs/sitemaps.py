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
    changefreq = "never"
    priority = 0.5

    def items(self):
        query_set = Post.published.for_blog(self.blog).filter(showing=Post.show_settings.everybody)
        return query_set

    def lastmod(self, post):
        return post.edited_on and post.edited_on or post.published_on

class CommentSitemap(BlogSitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Comment.published.for_object(self.blog)#FIXME: remove comments reg/private posts

    def lastmod(self, comment):
        return comment.edited_on and comment.edited_on or comment.created_on

class GlobalSitemap(Sitemap):
    pass
