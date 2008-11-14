# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^unsubscribe/(?P<user_id>\d+)/(?P<event_id>\d+)/$', 'turbion.notifications.views.unsubscribe', name="turbion_notifications_unsubscribe"),
)
