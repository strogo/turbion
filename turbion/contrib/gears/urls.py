from django.conf.urls.defaults import *
from turbion.gears.feeds import LatestGearsAtom

feeds = {
    'latest': LatestGearsAtom,
}

urlpatterns = patterns('django.contrib.syndication.views',
    url(r'^revolving/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}, "turbion_gears_feed"),
)
