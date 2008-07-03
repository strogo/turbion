# -*- coding: utf-8 -*-
#--------------------------------
#$Date: 2008-06-30 09:46:24 +0400 (Mon, 30 Jun 2008) $
#$Author: daev $
#$Revision: 18 $
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from turbion.blogs.sitemaps import BlogSitemap
from turbion.staticpages.models import Page

class PagesSitemap( BlogSitemap ):
    changefreq = "daily"
    priority = 0.5
    
    def items( self ):
        return Page.published.filter( blog = self.blog )