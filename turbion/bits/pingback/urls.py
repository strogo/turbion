from django.conf.urls.defaults import *

urlpatterns = patterns('turbion.core.pingback.views',
    url(r'^xmlrpc/(\d+)/$',           'gateway',   name="turbion_pingback_gateway"),
)
