from django.conf.urls.defaults import *

urlpatterns = patterns( 'turbion.pingback.views',
    url(r'^xmlrpc/(\d+)/$',                       'gateway',   name="turbion_pingback_gateway"),
)
