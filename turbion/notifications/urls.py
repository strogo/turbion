# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url( r'^unsubscribe/(?P<user_id>\d+)/(?P<event_id>\d+)/$', 'turbion.notifications.views.unsubscribe', name = "notifications_unsubscribe"),
    )
