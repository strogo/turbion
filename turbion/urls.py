from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.sitemaps.views import index, sitemap

from turbion.bits.profiles.models import Profile

# sitemaps
from turbion.bits.blogs.sitemaps import PostSitemap, CommentSitemap

sitemaps = {
    'posts': PostSitemap,
    'comments': CommentSitemap,
}

queryset = Profile.objects.filter(trusted=True).exclude(openid='').values_list('openid', flat=True)

urlpatterns = patterns('',
    url(r'^utils/',               include('turbion.bits.utils.urls')),
    url(r'^profiles/',            include('turbion.bits.profiles.urls')),
    url(r'^watchlist/',           include('turbion.bits.watchlist.urls')),
    url(r'^pingback/',            include('turbion.bits.pingback.urls')),
    url(r'^feedback/',            include('turbion.bits.feedback.urls')),
    url(r'^openid/',              include('turbion.bits.openid.urls')),
    url(r'^openid/whitelist/$',   'turbion.bits.whitelist.views.whitelist', {'queryset': queryset}, name='turbion_whitelist'),

    url(r'',                      include('turbion.bits.blogs.urls')),

    url(r'^sitemap\.xml$',        sitemap, {'sitemaps': sitemaps}, 'turbion_index_sitemap'),
    url(r'^sitemap_(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}, 'turbion_sitemap'),
)

from turbion import loading

loading.connectors()
