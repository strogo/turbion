# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.pingback.views',
    url(r'^xmlrpc/(?P<model>\d+)/(?P<id>\d+)/$',         'gateway', name="pingback_gateway"),
    url(r'^trackback/(?P<model_id>\d+)/(?P<id>\d+)/$',   'trackback'),
)
