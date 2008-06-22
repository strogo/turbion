# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from turbion.blogs import forms
from django.core.urlresolvers import reverse

def blog_globals( request ):
    if hasattr( request, "blog" ):
        blog = request.blog

        data = { 'blog_search_action' : reverse( "turbion.blogs.views.search.search", args = ( blog.slug, ) ), }

        return data
    return {}
