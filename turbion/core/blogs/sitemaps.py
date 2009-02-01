# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from turbion.core.blogs.models import Post, Comment

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        query_set = Post.published.filter(showing=Post.show_settings.everybody)
        return query_set

    def lastmod(self, post):
        return post.edited_on and post.edited_on or post.published_on

class CommentSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Comment.published.all()#FIXME: remove comments reg/private posts

    def lastmod(self, comment):
        return comment.edited_on and comment.edited_on or comment.created_on
