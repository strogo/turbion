# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.pingback.views',
        ( r'^xmlrpc/([-\._\w]+)/$',                              'gateway' ),
        ( r'^trackback/(?P<model_id>\d+)/(?P<id>\d+)/$',         'trackback' ),
    )
