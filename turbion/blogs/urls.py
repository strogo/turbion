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
from turbion.blogs.utils import blog_url

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

urlpatterns = patterns('turbion.blogs.views',
 ( r'^dashboard/',                          include( 'turbion.blogs.dashboard.urls' ) ),
 ( r'^profiles/',                           include( 'turbion.blogs.dashboard.urls' ) ),
)

if MULTIPLE_SETUP: #add global sitemap
    global_sitemap = { 'global' : GlobalSitemap }
    urlpatterns += patterns('', url( r'^sitemap.xml$', 'turbion.blogs.views.blog.index_sitemap', { 'sitemaps': global_sitemap }, "global_blog_sitemap" ) )

urlpatterns += patterns('turbion.blogs.views',
 blog_url( r'$',                                                'post.blog', name = "blog_index" ),

 blog_url( post_url_pattern + "$",                              'post.post', name = "blog_post" ),

 blog_url( r'(?P<post_id>\d+)/comment/add/$',                   'comment.add', name = "blog_comment_add" ),
 blog_url( r'comment/(?P<comment_id>\d+)/edit/$',               'comment.edit', name = "blog_comment_edit" ),

 blog_url( r'tags/$',                                           'post.tags', name = "blog_tags" ),
 blog_url( r'tag/(?P<tag_slug>[\w_-]+)/$',                      'post.tag' , name = "blog_tag" ),

 blog_url( r'archive/(?P<year_id>\d{4})/$',                                           'archive.year',  name = "blog_archive_year" ),
 blog_url( r'archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/$',                     'archive.month', name = "blog_archive_month" ),
 blog_url( r'archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/$', 'archive.day',   name = "blog_archive_day" ),

 blog_url( r'search/$',                                                               'search.search', name = "blog_search" ),
 blog_url( r'search/posts/$',                                                         'search.posts', name = "blog_search_posts"  ),
 blog_url( r'search/comments/$',                                                      'search.comments', name = "blog_search_comments" ),
 blog_url( r'feedback/',                                         include( 'turbion.feedback.urls' ) ),
)

urlpatterns += patterns('turbion.blogs.views',
 blog_url( r'feeds/atom/(?P<url>.*)/$',  'blog.feed',    { "feed_dict" : atom_feeds }, "blog_atom" ),
 blog_url( r'sitemap.xml$',              'blog.sitemap', { 'sitemaps': sitemaps },     "blog_sitemap" ),
)
