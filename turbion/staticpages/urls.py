# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *

from turbion.staticpages.sitemap import PagesSitemap

sitemaps = { "pages" : PagesSitemap }

urlpatterns = patterns( '',
    url( r'^(?P<slug>[\w_-]+)/$',    'turbion.staticpages.views.dispatcher', name = "pages_dispatcher" ),
    url( r'^sitemap.xml$',           'turbion.blogs.views.blog.sitemap', { 'sitemaps': sitemaps }, name = "pages_sitemap" ),
)
