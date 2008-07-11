# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

#global pages
urlpatterns = patterns('turbion.dashboard.views',
 url( r'^$',                                     'global.index',            name = "dashboard_index" ),
 url( r'^install/$',                             'global.install',          name = "dashboard_install" ),
 url( r'^create_superuser/$',                    'global.create_superuser', name = "dashboard_create_superuser" ),
 url( r'^create_blog/$',                         'global.create_blog',      name = "dashboard_create_blog" ),

 url( r'^login/$',                               'global.login',            name = "dashboard_login" ),
 url( r'^logout/$',                              'global.logout',           name = "dashboard_logout" ),

 url( r'^openid/',                               include( 'turbion.openid.urls' )  ),

 url( r'sources/posts/$',                        'sources.posts' ),
 url( r'sources/comments/$',                     'sources.comments' ),
 url( r'sources/users/$',                        'sources.users' ),
 url( r'^raw/',                                  include('django.contrib.admin.urls') ),
)

blog_slug = r"^(?P<blog>[\w_-]+)/"

def blog_url( regex, view, kwargs=None, name=None, prefix='' ):
    return url( blog_slug + regex, view, kwargs, name, prefix )

#blog specific pages
urlpatterns += patterns('turbion.dashboard.views',
 blog_url( r'$',                                     'blog.index',    name = "dashboard_blog_index" ),

 blog_url( r'posts/$',                               'blog.posts',    name = "dashboard_blog_posts" ),
 blog_url( r'post/new/$',                            'blog.post_new', name = "dashboard_blog_post_new" ),
 #url( r'^(?P<blog>[\w_-]+)/post/(?P<post_id>\d+)/$',               'blog.post' ),
 blog_url( r'post/(?P<post_id>\d+)/edit/$',          'blog.post_edit', name = "dashboard_blog_post_edit" ),
 blog_url( r'post/(?P<post_id>\d+)/delete/$',          'blog.post_edit', name = "dashboard_blog_post_edit" ),
 #url( r'^(?P<blog>[\w_-]+)/post/(?P<post_id>\d+)/status/(?P<status>\w+)/$',    'blog.post_status' ),

 #url( r'^(?P<blog>[\w_-]+)/comments/$',                            'blog.comments' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/$',         'blog.comment' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/edit/$',    'blog.comment_edit' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/status/$',  'blog.comment_status' ),

 #url( r'^(?P<blog>[\w_-]+)/preferences/$',                         'blog.preferences' ),

 #blog_url( r'assets/$',                              'assets.index' ),
 #blog_url( r'assets/new/$',                           'assets.new' ),
 #blog_url( r'assets/(?P<asset_id>\d+)/edit/$',        'assets.edit' ),
 blog_url( r'pages/$',                                'pages.pages', name = "dashboard_blog_pages" ),

 blog_url( r'feedbacks/$',                            'feedback.feedbacks', name = "dashboard_blog_feedbacks" ),
 blog_url( r'feedbacks/new/$',                        'feedback.new',       name = "dashboard_blog_feedbacks_new" ),
 blog_url( r'feedbacks/(?P<feedback_id>\d+)/edit/$',  'feedback.edit',      name = "dashboard_blog_feedbacks_edit" ),
 blog_url( r'feedbacks/(?P<feedback_id>\d+)/delete/$','feedback.delete',    name = "dashboard_blog_feedbacks_delete" ),
)
