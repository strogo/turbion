# -*- coding: utf-8 -*-
from turbion.blogs.sitemaps import Sitemap

from turbion.profiles.models import Profile

class ProfilesSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5    
    
    def items(self):
        return Profile.public.all()
    
    def location(self, profile):
        return profile.get_public_url()
