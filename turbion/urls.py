from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.sitemaps.views import index, sitemap

# sitemaps
from turbion.core.blogs.sitemaps import PostSitemap, CommentSitemap

sitemaps = {
    'posts': PostSitemap,
    'comments': CommentSitemap,
}

urlpatterns = patterns('',
    url(r'^utils/',               include('turbion.core.utils.urls')),
    url(r'^profile/',             include('turbion.core.profiles.urls')),
    url(r'^notifications/',       include('turbion.core.notifications.urls')),
    url(r'^pingback/',            include('turbion.core.pingback.urls')),

    url(r'',                      include('turbion.core.blogs.urls')),

    url(r'^sitemap\.xml$',        sitemap, {'sitemaps': sitemaps}, 'turbion_index_sitemap'),
    url(r'^sitemap_(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}, 'turbion_sitemap'),
)

from turbion import loading

loading.connectors()
