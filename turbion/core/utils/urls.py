from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

from turbion.core.utils import antispam

def uri_reverse(view, urlconf=None, args=None, kwargs=None):
    from django.contrib.sites.models import Site

    domain = Site.objects.get_current().domain

    return "http://%s%s" % (domain, reverse(view, urlconf, args, kwargs))

urlpatterns = patterns('',
    url(r'^status/',     "turbion.core.utils.views.status", name="turbion_status"),
)

urlpatterns += antispam.urlpatterns
