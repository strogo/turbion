# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.staticpages.views',
    url( r'(?P<slug>[\w_-]+)/$',        'dispatcher', name = "pages_dispatcher" ),
)
