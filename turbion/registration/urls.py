# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.registration.views',
    ( r'^$',                           'registration' ),
    ( r'^confirm/$',                   'registration_confirm' ),
    
    ( r'^change/email/$',              'change_email' ),
    ( r'^change/email/confirm/$',      'change_email_confirm' ),
    ( r'^change/password/$',           'change_password' ),
    
    ( r'^restore/$',                   'restore_password' ),
    ( r'^restore/request/$',           'restore_password_request' ),
    
    ( r'^login/$',                     'login' ),
    ( r'^logout/$',                    'logout' ),
)