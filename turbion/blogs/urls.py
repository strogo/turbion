# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *
from django.conf import settings

from turbion.blogs import feeds
from turbion.blogs.sitemaps import PostSitemap, CommentSitemap, GlobalSitemap
from turbion.blogs.decorators import *
from turbion.blogs import utils

MULTIPLE_SETUP = getattr( settings, 'BLOGS_MULTIPLE', False )

atom_feeds = {
    'posts'   : feeds.PostsFeedAtom,
    'comments': feeds.CommentsFeedAtom,
    'tag'     : feeds.TagFeedAtom,
}

sitemaps = {
    'posts'    : PostSitemap,
    'comments' : CommentSitemap
}

post_url_pattern = r"post/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/(?P<post_slug>[\w_-]+)/"

if MULTIPLE_SETUP:
    blog_slug = r"^(?P<blog>[\w_-]+)/"
else:
    blog_slug = r"^"

urlpatterns = patterns('turbion.blogs.views',
 ( r'^dashboard/',                               include( 'turbion.blogs.dashboard.urls' ) ),
 ( r'^profiles/',                                include( 'turbion.blogs.dashboard.urls' ) ),
)

if MULTIPLE_SETUP: #add global sitemap
    global_sitemap = { 'global' : GlobalSitemap }
    urlpatterns += patterns('', url( r'^sitemap.xml$', 'turbion.blogs.views.blog.index_sitemap', { 'sitemaps': global_sitemap }, "global_blog_sitemap" ) )

urlpatterns += patterns('turbion.blogs.views',
 url( blog_slug + r'$',                                                'post.blog', name = "blog_index" ),

 url( blog_slug + post_url_pattern + "$",                              'post.post', name = "blog_post" ),

 url( blog_slug + r'(?P<post_id>\d+)/comment/add/$',                   'comment.add', name = "blog_comment_add" ),
 url( blog_slug + r'comment/(?P<comment_id>\d+)/edit/$',               'comment.edit', name = "blog_comment_edit" ),

 url( blog_slug + r'tags/$',                                           'post.tags', name = "blog_tags" ),
 url( blog_slug + r'tag/(?P<tag_slug>[\w_-]+)/$',                      'post.tag' , name = "blog_tag" ),

 url( blog_slug + r'archive/(?P<year_id>\d{4})/$',                                           'archive.year',  name = "blog_archive_year" ),
 url( blog_slug + r'archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/$',                     'archive.month', name = "blog_archive_month" ),
 url( blog_slug + r'archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/$', 'archive.day',   name = "blog_archive_day" ),

 url( blog_slug + r'search/$',                                                               'search.search', name = "blog_search" ),
 url( blog_slug + r'search/posts/$',                                                         'search.posts', name = "blog_search_posts"  ),
 url( blog_slug + r'search/comments/$',                                                      'search.comments', name = "blog_search_comments" ),
 url( blog_slug + r'feedback/',                                         include( 'turbion.feedback.urls' ) ),
)

urlpatterns += patterns('turbion.blogs.views',
 url( blog_slug + r'feeds/atom/(?P<url>.*)/$',  'blog.feed',    { "feed_dict" : atom_feeds }, "blog_atom" ),
 url( blog_slug + r'sitemap.xml$',              'blog.sitemap', { 'sitemaps': sitemaps },     "blog_sitemap" ),
)
