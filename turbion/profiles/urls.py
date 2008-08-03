# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.profiles.views',
    url( r'^(?P<profile_user>[\w_-]+)/$',                        'profile',      name = "profile_index" ),
    url( r'^(?P<profile_user>[\w_-]+)/edit/$',                   'edit_profile', name = "profile_edit" ),
)
