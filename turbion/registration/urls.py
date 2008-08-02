# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.registration.views',
    url(r'^$',                           'registration',         name = "registration_index"),
    url(r'^confirm/$',                   'registration_confirm', name = "registration_confirm"),

    url(r'^change/email/$',              'change_email'),
    url(r'^change/email/confirm/$',      'change_email_confirm'),
    url(r'^change/password/$',           'change_password'),

    url(r'^restore/$',                   'restore_password'),
    url(r'^restore/request/$',           'restore_password_request'),
)
