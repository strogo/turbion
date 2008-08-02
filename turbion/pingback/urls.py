# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.pingback.views',
        ( r'^xmlrpc/([-\._\w]+)/$',                              'gateway' ),
        ( r'^trackback/(?P<model_id>\d+)/(?P<id>\d+)/$',         'trackback' ),
    )
