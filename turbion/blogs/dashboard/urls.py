# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

#global pages
urlpatterns = patterns('turbion.blogs.dashboard.views',
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

#blog specific pages
urlpatterns += patterns('turbion.blogs.dashboard.views',
 url( r'^(?P<blog>[\w_-]+)/$',                                     'blog.index',    name = "dashboard_blog_index" ),

 url( r'^(?P<blog>[\w_-]+)/posts/$',                               'blog.posts',    name = "dashboard_blog_posts" ),
 url( r'^(?P<blog>[\w_-]+)/post/new/$',                            'blog.post_new', name = "dashboard_blog_post_new" ),
 #url( r'^(?P<blog>[\w_-]+)/post/(?P<post_id>\d+)/$',               'blog.post' ),
 url( r'^(?P<blog>[\w_-]+)/post/(?P<post_id>\d+)/edit/$',          'blog.post_edit', name = "dashboard_blog_post_edit" ),
 #url( r'^(?P<blog>[\w_-]+)/post/(?P<post_id>\d+)/status/(?P<status>\w+)/$',    'blog.post_status' ),

 #url( r'^(?P<blog>[\w_-]+)/comments/$',                            'blog.comments' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/$',         'blog.comment' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/edit/$',    'blog.comment_edit' ),
 #url( r'^(?P<blog>[\w_-]+)/comment/(?P<comment_id>\d+)/status/$',  'blog.comment_status' ),

 #url( r'^(?P<blog>[\w_-]+)/preferences/$',                         'blog.preferences' ),

 #url( r'^(?P<blog>[\w_-]+)/assets/$',                              'assets.index' ),
 #url( r'^(?P<blog>[\w_-]+)/asset/new/$',                           'assets.new' ),
 #url( r'^(?P<blog>[\w_-]+)/asset/(?P<asset_id>\d+)/edit/$',        'assets.edit' ),

 #( r'^preference/$',                                                          'preference.edit' ),
)
