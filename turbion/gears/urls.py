# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.conf.urls.defaults import *
from turbion.gears.feeds import *

feeds = {
    'latest': LatestGearsAtom,
}

urlpatterns = patterns('',
        ( r'^revolving/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, "gears_feed"),
    )
