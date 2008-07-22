# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2008 Alexander Koshelev (daevaorn@gmail.com)
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from turbion.blogs.decorators import blog_view, post_view
from turbion.staticpages.models import Page
from turbion.blogs.models import BlogRoles
from turbion.roles.decorators import has_capability_for

from pantheon.utils.decorators import titled, templated

@never_cache
@blog_view
@templated( "turbion/dashboard/feedback/feedbacks.html")
@titled( page = "Select page", section = "Pages" )
@has_capability_for( BlogRoles.capabilities.review_feedback, "blog" )
def pages( request, blog ):
    pages = Page.objects.filter( blog = blog )

    return { "blog" : blog,
             "pages" : pages }
