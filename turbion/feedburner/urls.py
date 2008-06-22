# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.feedburner.views',
    ( r'^create/(?P<id>\d+)/$',                  'add_to_feedburner' ),
)