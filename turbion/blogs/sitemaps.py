# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.sitemaps import Sitemap, ping_google
from turbion.blogs.models import Post, Comment

from django.utils.functional import curry
from django.db.models import signals
from django.dispatch import dispatcher
from django.conf import settings
from django.core.urlresolvers import reverse

class BlogSitemap( Sitemap ):
    def __init__( self, blog ):
        self.blog = blog

class PostSitemap( BlogSitemap ):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return Post.published.for_blog( self.blog )

    def lastmod(self, post):
        return post.edited_on

class CommentSitemap( BlogSitemap ):
    changefreq = "always"
    priority = 0.5

    def items( self ):
        return Comment.published.for_object( self.blog )

    def lastmod( self, comment):
        return comment.date

class GlobalSitemap( Sitemap ):
    pass

def post_save(instance):
    try:
        if instance.is_published():
            ping_google()
    except Exception:
        pass

def comment_save(instance):
    try:
        if instance.blog_posts.count():
            ping_google()
    except Exception:
        pass

if settings.ON_SERVER:
    dispatcher.connect( post_save,    signal = signals.post_save, sender = Post )
    dispatcher.connect( comment_save, signal = signals.post_save, sender = Comment )
