from django.conf.urls.defaults import *
from django.contrib.sitemaps.views import index, sitemap

from turbion import admin

# sitemaps
from turbion.core.blogs.sitemaps import PostSitemap, CommentSitemap
from turbion.core.staticpages.sitemap import PagesSitemap
from turbion.core.profiles.sitemap import ProfilesSitemap

sitemaps = {
    'posts': PostSitemap,
    'comments': CommentSitemap,
    'pages': PagesSitemap,
    'profiles': ProfilesSitemap,
}

urlpatterns = patterns('',
    url(r'^dashboard/(.*)',       admin.site.root, name='turbion_admin_root'),
    url(r'^utils/',               include('turbion.core.utils.urls')),
    url(r'^profile/',             include('turbion.core.profiles.urls')),
    url(r'^notifications/',       include('turbion.core.notifications.urls')),
    url(r'^staticpages/',         include('turbion.core.staticpages.urls')),

    url(r'',                      include('turbion.core.blogs.urls')),

    url(r'^sitemap\.xml$',        sitemap, {'sitemaps': sitemaps}, 'turbion_index_sitemap'),
    url(r'^sitemap_(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}, 'turbion_sitemap'),
)

from turbion import loading

loading.admins()
loading.connectors()
