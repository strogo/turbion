from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from turbion.core.watchlist.feeds import UserFeed

feed_dict = {
    'atom': UserFeed
}

urlpatterns = patterns('turbion.core.watchlist.views',
    url(r'/$', 'watchlist', name='turbion_watchlist'),
    url(r'/add/$', 'add_to_watchlist', name='turbion_watchlist_add'),
    url(r'/update/$', 'update_watchlist', name='turbion_watchlist_update'),
    url(r'/feed/(.+)$', feed, {'feed_dict': feed_dict}, name='turbion_watchlist_feed',),
    url(r'^(\d+)/unsubscribe/$', 'unsubscribe', name="turbion_watchlist_unsubscribe"),
)
