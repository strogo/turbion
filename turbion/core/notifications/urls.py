from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.core.notifications.views',
    url(r'^unsubscribe/(?P<user_id>\d+)/(?P<event_id>\d+)/$', 'unsubscribe', name="turbion_notifications_unsubscribe"),
)
