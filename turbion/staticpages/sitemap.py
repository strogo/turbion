# -*- coding: utf-8 -*-
from turbion.blogs.sitemaps import BlogSitemap
from turbion.staticpages.models import Page

class PagesSitemap( BlogSitemap ):
    changefreq = "daily"
    priority = 0.5

    def items( self ):
        return Page.published.filter( blog = self.blog )
