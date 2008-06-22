# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.pingback.views', 
        ( r'^xmlrpc/([-\._\w]+)/$',                                 'gateway' ),
        ( r'^trackback/(?P<model>[-\._\w]+)/(?P<id>\d+)/$',         'trackback' ),
    )
