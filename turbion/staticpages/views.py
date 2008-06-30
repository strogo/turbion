# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from pantheon.utils.decorators import templated, titled

from turbion.staticpages.models import Page
from turbion.blogs.decorators import blog_view

@templated( 'turbion/staticpages/generic.html' )
@titled( page = u"{{page.title}}" )
@blog_view
def dispatcher( request, blog, slug ):
    page = get_object_or_404( Page.published, blog = blog, slug = slug )
    return { "page" : page,
             "blog" : blog }, page.template or 'turbion/staticpages/generic.html'
