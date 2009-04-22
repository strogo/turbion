from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from turbion.core.watchlist.feeds import UserWatchlistFeed

feed_dict = {
    'atom': UserWatchlistFeed
}

urlpatterns = patterns('turbion.core.watchlist.views',
    url(r'^$', 'index', name='turbion_watchlist'),
    url(r'^add/$', 'add_to_watchlist', name='turbion_watchlist_add'),
    url(r'^update/$', 'update_watchlist', name='turbion_watchlist_update'),
    url(r'^feed/(.+)$', feed, {'feed_dict': feed_dict}, name='turbion_watchlist_feed',),
    url(r'^unsubscribe/(\d+)/$', 'unsubscribe', name="turbion_watchlist_unsubscribe"),
)
