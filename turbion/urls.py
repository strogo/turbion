# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *
from django.conf import settings

from turbion.blogs.utils import blog_url

urlpatterns = patterns('',
    url( r'^profile/',                      include( 'turbion.profiles.urls' ) ),#FIXME: remove profile link
    url( r'^captcha/(?P<id>\w+)/$',         "pantheon.supernovaforms.views.captcha_image" ),
    url( r'^pingback/',                     include( 'turbion.pingback.urls' )  ),
    url( r'^notifications/',                include( 'turbion.notifications.urls' )  ),
    #url( r'^feedburner/',                   include( 'turbion.feedburner.urls' )  ),
    url( r'^roles/',                        include( 'turbion.roles.urls' )  ),
    url( r'^comments/',                     include( 'turbion.comments.urls' )  ),
    url( r'^gears/',                        include( 'turbion.gears.urls' )  ),
    url( r'^registration/',                 include( 'turbion.registration.urls' )  ),
    url( r'^dashboard/',                    include( 'turbion.dashboard.urls' ) ),

    blog_url( r'',                          include( 'turbion.blogs.urls' ) ),
    blog_url( r'pages/',                    include( 'turbion.staticpages.urls' ) ),
    blog_url( r'feedback/',                 include( 'turbion.feedback.urls' ) ),
)

MULTIPLE_SETUP = getattr( settings, 'TRUBION_BLOGS_MULTIPLE', False )

if MULTIPLE_SETUP:
    urlpatterns += patterns('', url( r'^sitemap.xml$', 'turbion.blogs.views.blog.index_sitemap', name = "global_blog_sitemap" ) )