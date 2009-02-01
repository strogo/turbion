# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w_-]+)/$',  'turbion.core.staticpages.views.dispatcher', name="turbion_pages_dispatcher"),
)
