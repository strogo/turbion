# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

def uri_reverse(view, urlconf=None, args=None, kwargs=None):
    from django.contrib.sites.models import Site

    domain = Site.objects.get_current().domain

    return "http://%s%s" % (domain, reverse(view, urlconf, args, kwargs))

urlpatterns = patterns('',
    url( r'^captcha/(?P<id>\w+)/$',  "turbion.core.utils.captcha.views.image", name="turbion_captcha_image"),
    url( r'^status/',                "turbion.core.utils.views.status",        name="turbion_status"),
)