# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url( r'^pages/(?P<slug>[\w_-]+)/$',     'turbion.staticpages.views.dispatcher', name = "pages" ),
    url( r'^profile/',                      include( 'turbion.profiles.urls' ) ),
    url( r'^captcha/(?P<id>\w+)/$',         "pantheon.supernovaforms.views.captcha_image" ),


    url( r'^pingback/',                     include( 'turbion.pingback.urls' )  ),
    url( r'^notifications/',                include( 'turbion.notifications.urls' )  ),
    url( r'^feedburner/',                   include( 'turbion.feedburner.urls' )  ),
    url( r'^roles/',                        include( 'turbion.roles.urls' )  ),
    url( r'^comments/',                     include( 'turbion.comments.urls' )  ),
    url( r'^gears/',                        include( 'turbion.gears.urls' )  ),

    url( r'^',                              include( 'turbion.blogs.urls' ),        name = "blog_root" ),
)
