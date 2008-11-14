# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.openid.views',
    url(r'^login/$',                 'authorization.login',        name="turbion_openid_login"),
    url(r'^authenticate/$',          'authorization.authenticate', name="turbion_openid_authenticate"),
    url(r'^collect/$',               'authorization.collect',      name="turbion_openid_collect"),

    url(r'^server/endpoint/$',       'server.endpoint',    name="turbion_openid_endpoint"),
    url(r'^server/decide/$',         'server.decide',      name="turbion_openid_decide"),
    url(r'^server/xrds/$',           'server.xrds',        name="turbion_openid_xrds"),

    url(r'^list/$',                  'management.list',    name="turbion_openid_list"),
    url(r'^add/$',                   'management.add',     name="turbion_openid_add"),
    url(r'^delete/(?P<id>\d+)/$',    'management.delete',  name="turbion_openid_delete"),
)
