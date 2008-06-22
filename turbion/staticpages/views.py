# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from pantheon.utils.decorators import title_bits, render_to
from turbion.staticpages.models import Page

@title_bits( page = u"{{page.title}}" )
@render_to( 'staticpages/generic.html' )
def dispatcher( request, slug ):
    page = get_object_or_404( Page, slug = slug )    
    return { "page" : page }, page.template or 'staticpages/generic.html'