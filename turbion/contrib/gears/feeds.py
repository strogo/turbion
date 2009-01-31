# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from turbion.utils.title import gen_title
from turbion.gears.gear import GearSpot

class LatestGearsAtom(Feed):
    feed_type = Atom1Feed

    def item_pubdate(self, info):
        return info.get_last_time()

    def title(self):
        return gen_title({
            "page": _("Latest revolving gears"),
            "section": _("Gears")
        })

    def description(self):
        return _("Latest revolving gears")

    def link(self, obj=None):
        return "/"
    item_link = link

    def item_guid(self, info):
        return "<gear: %s>" % info._get_pk_val()

    def items(self):
        return GearSpot.revolve_all()
