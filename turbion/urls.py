from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.sitemaps.views import index, sitemap

from turbion.core.profiles.models import Profile

# sitemaps
from turbion.core.blogs.sitemaps import PostSitemap, CommentSitemap

sitemaps = {
    'posts': PostSitemap,
    'comments': CommentSitemap,
}

queryset = Profile.objects.filter(trusted=True).exclude(openid='').values_list('openid', flat=True)

urlpatterns = patterns('',
    url(r'^utils/',               include('turbion.core.utils.urls')),
    url(r'^profiles/',            include('turbion.core.profiles.urls')),
    url(r'^watchlist/',           include('turbion.core.watchlist.urls')),
    url(r'^pingback/',            include('turbion.core.pingback.urls')),
    url(r'^feedback/',            include('turbion.core.feedback.urls')),
    url(r'^openid/',              include('turbion.core.openid.urls')),
    url(r'^openid/whitelist/$',   'turbion.core.whitelist.views.whitelist', {'queryset': queryset}, name='turbion_whitelist'),

    url(r'',                      include('turbion.core.blogs.urls')),

    url(r'^sitemap\.xml$',        sitemap, {'sitemaps': sitemaps}, 'turbion_index_sitemap'),
    url(r'^sitemap_(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}, 'turbion_sitemap'),
)

from turbion import loading

loading.connectors()
