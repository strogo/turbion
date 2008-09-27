# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.openid.views',
    url(r'^login/$',                      'authorization.login',        name="openid_login"),
    url(r'^authenticate/$',               'authorization.authenticate', name="openid_authenticate"),
    url(r'^collect/$',                    'authorization.collect' ),

    (r'^list/$',                       'management.list'),
    (r'^add/$',                        'management.add'),
    (r'^delete/(?P<id>\d+)/$',         'management.delete'),
)
