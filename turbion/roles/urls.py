# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

#global pages
urlpatterns = patterns('turbion.roles.views',
    url( "^no_capability/$", "no_capability", name = "no_capability" ),
)
