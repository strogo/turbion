# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.openid.views',
    ( r'^login/$',                      'login' ),
    ( r'^authenticate/$',               'authenticate' ),
    ( r'^collect/$',                    'collect' ),
    
    ( r'^list/$',                       'list' ),
    ( r'^add/$',                        'add' ),
    ( r'^delete/(?P<id>\d+)/$',         'delete' ),
)