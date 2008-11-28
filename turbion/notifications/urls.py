# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.notifications.views',
    url(r'^unsubscribe/(?P<user_id>\d+)/(?P<event_id>\d+)/$', 'unsubscribe', name="turbion_notifications_unsubscribe"),
)
