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
    blog_url( r'pages/',                    include( 'turbion.staticpages.urls' ) ),
    blog_url( r'feedback/',                 include( 'turbion.feedback.urls' ) ),
    url( r'^profile/',                      include( 'turbion.profiles.urls' ) ),#FIXME: remove profile link
    url( r'^captcha/(?P<id>\w+)/$',         "pantheon.supernovaforms.views.captcha_image" ),

    url( r'^pingback/',                     include( 'turbion.pingback.urls' )  ),
    url( r'^notifications/',                include( 'turbion.notifications.urls' )  ),
    url( r'^feedburner/',                   include( 'turbion.feedburner.urls' )  ),
    url( r'^roles/',                        include( 'turbion.roles.urls' )  ),
    url( r'^comments/',                     include( 'turbion.comments.urls' )  ),
    url( r'^gears/',                        include( 'turbion.gears.urls' )  ),
    url( r'^openid/',                       include( 'turbion.openid.urls' )  ),

    url( r'^',                              include( 'turbion.blogs.urls' ),        name = "blog_root" ),
)
