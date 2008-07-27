# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *
from django.conf import settings

from turbion.blogs import feeds
from turbion.blogs.sitemaps import PostSitemap, CommentSitemap, GlobalSitemap
from turbion.blogs.utils import blog_url

atom_feeds = {
    'posts'   : feeds.PostsFeedAtom,
    'comments': feeds.CommentsFeedAtom,
    'tag'     : feeds.TagFeedAtom,
}

sitemaps = {
    'posts'    : PostSitemap,
    'comments' : CommentSitemap
}

post_url_pattern = r"^%s(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/(?P<post_slug>[\w_-]+)/" % settings.TURBION_POST_PERMALINK_PREFIX.lstrip('/')

urlpatterns = patterns('turbion.blogs.views',
 url( r'^$',                                                'post.blog', name = "blog_index" ),

 url( post_url_pattern + "$",                              'post.post', name = "blog_post" ),

 url( r'^post/(?P<post_id>\d+)/comment/add/$',              'comment.add', name = "blog_comment_add" ),
 url( r'^comment/(?P<comment_id>\d+)/edit/$',               'comment.edit', name = "blog_comment_edit" ),

 url( r'^tags/$',                                           'post.tags', name = "blog_tags" ),
 url( r'^tag/(?P<tag_slug>[\w_-]+)/$',                      'post.tag' , name = "blog_tag" ),

 url( r'^archive/(?P<year_id>\d{4})/$',                                           'archive.year',  name = "blog_archive_year" ),
 url( r'^archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/$',                     'archive.month', name = "blog_archive_month" ),
 url( r'^archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/$', 'archive.day',   name = "blog_archive_day" ),

 url( r'^search/$',                                                               'search.search', name = "blog_search" ),
 url( r'^search/posts/$',                                                         'search.posts', name = "blog_search_posts"  ),
 url( r'^search/comments/$',                                                      'search.comments', name = "blog_search_comments" ),
)

urlpatterns += patterns('turbion.blogs.views',
 url( r'^feeds/atom/(?P<url>.*)/$',  'blog.feed',    { "feed_dict" : atom_feeds }, "blog_atom" ),
 url( r'^sitemap.xml$',              'blog.sitemap', { 'sitemaps': sitemaps },     "blog_sitemap" ),
)
