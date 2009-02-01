# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.syndication.views import feed

from turbion.core.blogs import feeds

atom_feeds = {
    'posts'   : feeds.PostsFeedAtom,
    'comments': feeds.CommentsFeedAtom,
    'tag'     : feeds.TagFeedAtom,
}

rss_feeds = {
    'posts'   : feeds.PostsFeed,
    'comments': feeds.CommentsFeed,
    'tag'     : feeds.TagFeed,
}

urlpatterns = patterns('turbion.core.blogs.views',
 url(r'^$',                                  'post.blog', name="turbion_blog_index"),

 url(r"^(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/"
     r"(?P<post_slug>[\w_-]+)/$",            'post.post', name="turbion_blog_post"),

 url(r'^p/(?P<post_id>\d+)/comment/add/$',   'comment.add', name="turbion_blog_comment_add"),
 url(r'^comment/(?P<comment_id>\d+)/edit/$', 'comment.edit', name="turbion_blog_comment_edit"),

 url(r'^tags/$',                             'post.tags', name="turbion_blog_tags"),
 url(r'^tag/(?P<tag_slug>[\w_-]+)/$',        'post.tag' , name="turbion_blog_tag"),

 url(r'^archive/$',                          'archive.index', name="turbion_blog_archive"),
 url(r'^archive/(?P<year_id>\d{4})/$',       'archive.year',  name="turbion_blog_archive_year"),
 url(r'^archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/$',  'archive.month', name="turbion_blog_archive_month"),
 url(r'^archive/(?P<year_id>\d{4})/(?P<month_id>\d{1,2})/(?P<day_id>\d{1,2})/$', 'archive.day',   name="turbion_blog_archive_day"),
)

if "djapian" in settings.INSTALLED_APPS:
    urlpatterns += patterns('turbion.core.blogs.views',
     url(r'^search/$',            'search.search',   name="turbion_blog_search"),
     url(r'^search/posts/$',      'search.posts',    name="turbion_blog_search_posts"),
     url(r'^search/comments/$',   'search.comments', name="turbion_blog_search_comments"),
    )

urlpatterns += patterns('',
 url(r'^feeds/rss/(?P<url>.*)/$',   feed,    {"feed_dict": rss_feeds}, "turbion_blog_rss"),
 url(r'^feeds/atom/(?P<url>.*)/$',  feed,    {"feed_dict": atom_feeds},"turbion_blog_atom"),
)
