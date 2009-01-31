# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from turbion.core.profiles.sitemap import ProfilesSitemap

sitemaps = {
    "profiles": ProfilesSitemap,
}

urlpatterns = patterns( 'turbion.core.profiles.views',
    url(r'^(?P<profile_user>[\w_-]+)/$',       'profile',      name="turbion_profile_index"),
    url(r'^(?P<profile_user>[\w_-]+)/edit/$',  'edit_profile', name="turbion_profile_edit"),
)

urlpatterns += patterns('django.contrib.sitemaps.views',
    url(r'^sitemap.xml$',     'sitemap', {"sitemaps": sitemaps}, name="turbion_profiles_sitemap"),
)
