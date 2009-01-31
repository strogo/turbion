# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from turbion.core.staticpages.sitemap import PagesSitemap

sitemaps = {"pages": PagesSitemap}

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w_-]+)/$',  'turbion.core.staticpages.views.dispatcher', name="turbion_pages_dispatcher"),
    url(r'^sitemap.xml$',         'turbion.core.blogs.views.blog.sitemap', {'sitemaps': sitemaps}, name="turbion_pages_sitemap"),
)
