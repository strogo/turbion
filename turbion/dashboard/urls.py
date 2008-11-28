# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

#global pages
urlpatterns = patterns('turbion.dashboard.views',
 url(r'^$',                                     'global.index',            name="turbion_dashboard_index"),
 url(r'^install/$',                             'global.install',          name="turbion_dashboard_install"),
 url(r'^create_superuser/$',                    'global.create_superuser', name="turbion_dashboard_create_superuser"),
 url(r'^create_blog/$',                         'global.create_blog',      name="turbion_dashboard_create_blog"),

 url(r'^login/$',                               'global.login',            name="turbion_dashboard_login"),
 url(r'^logout/$',                              'global.logout',           name="turbion_dashboard_logout"),

 url(r'^openid/',                               include('turbion.openid.urls')),
)

blog_slug = r"^(?P<blog>[\w_-]+)/"

def blog_url(regex, view, kwargs=None, name=None, prefix=''):
    return url(blog_slug + regex, view, kwargs, name, prefix)

#blog specific pages
urlpatterns += patterns('turbion.dashboard.views',
 blog_url(r'$',                                       'blog.dashbaord', name="turbion_dashboard_blog_index"),

 blog_url(r'sources/(?P<name>[\w_-]+)/$',             'sources.source', name="turbion_dashboard_sources"),
 blog_url(r'sources/(?P<name>[\w_-]+)/schema/$',      'sources.schema', name="turbion_dashboard_sources_schema"),

 blog_url(r'posts/$',                                 'blog.index',     name="turbion_dashboard_blog_posts"),
 blog_url(r'post/new/$',                              'blog.post_new',  name="turbion_dashboard_blog_post_new"),
 #blog_url(r'post/(?P<post_id>\d+)/$',                'blog.post' ),
 blog_url(r'post/(?P<post_id>\d+)/edit/$',            'blog.post_edit', name="turbion_dashboard_blog_post_edit"),
 blog_url(r'post/(?P<post_id>\d+)/delete/$',          'blog.post_edit', name="turbion_dashboard_blog_post_delete"),

 #blog_url(r'comments/$',                             'blog.comments'),
 #blog_url(r'comment/(?P<comment_id>\d+)/$',          'blog.comment'),
 #blog_url(r'comment/(?P<comment_id>\d+)/edit/$',     'blog.comment_edit'),
 #blog_url(r'comment/(?P<comment_id>\d+)/status/$',   'blog.comment_status'),

 blog_url(r'assets/$',                               'assets.index',  name="turbion_dashboard_blog_assets"),
 blog_url(r'assets/new/$',                           'assets.edit',   name="turbion_dashboard_blog_assets_new"),
 blog_url(r'assets/(?P<asset_id>\d+)/edit/$',        'assets.edit',   name="turbion_dashboard_blog_assets_edit"),
 blog_url(r'assets/(?P<asset_id>\d+)/delete/$',      'assets.delete', name="turbion_dashboard_blog_assets_delete"),

 blog_url(r'pages/$',                                'pages.pages', name="turbion_dashboard_blog_pages"),

 blog_url(r'feedbacks/$',                            'feedback.feedbacks', name="turbion_dashboard_blog_feedbacks"),
 blog_url(r'feedbacks/(?P<feedback_id>\d+)/edit/$',  'feedback.edit',      name="turbion_dashboard_blog_feedback_edit"),
 blog_url(r'feedbacks/(?P<feedback_id>\d+)/delete/$','feedback.delete',    name="turbion_dashboard_blog_feedback_delete"),
)
