# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.registration.views',
    url(r'^$',                           'registration',         name="turbion_registration_index"),
    url(r'^confirm/$',                   'registration_confirm', name="turbion_registration_confirm"),

    url(r'^change/email/$',              'change_email',         name="turbion_change_email"),
    url(r'^change/email/confirm/$',      'change_email_confirm', name="turbion_change_email_confirm"),

    url(r'^change/password/$',           'change_password',      name="turbion_change_password"),

    url(r'^restore/request/$',           'restore_password_request', name="turbion_restore_password_request"),
    url(r'^restore/$',                   'restore_password',     name="turbion_restore_password"),
)
