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
from turbion.feedback.models import Feedback

from pantheon.utils.decorators import titled, templated

@never_cache
@blog_view
@templated( "turbion/feedback/dashboard/feedbacks.html")
@titled()
def feedbacks( request, blog ):


    return { "blog" : blog }

@never_cache
@blog_view
def new( request, blog ):
    pass

@never_cache
@blog_view
def edit( request, blog, feedback_id ):
    feedback = get_object_or_404( Feedback, pk = feedback_id )

@never_cache
@blog_view
def delete( request, blog, feedback_id ):
    get_object_or_404( Feedback, pk = feedback_id ).delete()
