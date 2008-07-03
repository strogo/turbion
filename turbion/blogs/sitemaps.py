# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.sitemaps import Sitemap
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
