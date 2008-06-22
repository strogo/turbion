# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from pantheon.utils.title import gen_title
from django.shortcuts import *
from django.core.urlresolvers import reverse

class LatestGearsAtom( Feed ):
    feed_type = Atom1Feed

    def get_object(self, bits):
        if len(bits) == 1:
            return get_object_or_404( Tag, slug = bits[ 0 ] )
        raise Http404

    def item_link( self, link ):
        return link.get_absolute_url()

    def item_pubdate( self, link ):
        return link.date

    def title(self,obj):
        return gen_title( { "page":u"Новые" + ( obj and u" c тегом '%s'" % obj or "" ), "section":u"Ссылки" } )

    def link(self,obj):
        return obj and reverse( "turbion.links.views.tag", kwargs={ "slug" : obj.slug } ) or reverse( "turbion.links.views.index" )

    def description( self, obj ):
        return "Новые ссылки" + ( obj and " c тегом '%s'" % obj or "" )

    def items( self, obj ):
        man = obj and Link.active.for_tag( obj ) or Link.active.all()
        return man.order_by( "-date" )
