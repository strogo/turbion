# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

#global pages
urlpatterns = patterns('turbion.roles.views',
    url( "^no_capability/$", "no_capability", name = "no_capability" ),
)
