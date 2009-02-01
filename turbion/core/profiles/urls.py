# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.core.profiles.views',
    url(r'^(?P<profile_user>[\w_-]+)/$',       'profile',      name="turbion_profile_index"),
    url(r'^(?P<profile_user>[\w_-]+)/edit/$',  'edit_profile', name="turbion_profile_edit"),
)
