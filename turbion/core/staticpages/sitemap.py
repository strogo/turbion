# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from turbion.core.staticpages.models import Page

class PagesSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Page.published.all()
