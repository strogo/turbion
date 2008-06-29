# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import *

import re

from turbion.blogs.models import Blog, Post, BlogRoles
from turbion.registration.models import IllegalName

from pantheon.utils.decorators import special_titled

titled = special_titled( section = u"{{blog.name}}" )

def blog_view( view_func ):
    """
    Picks up blog slug and `converts` it into blog object
    """
    def _decor( request, blog = None, *args, **kwargs ):
        if blog is not None:
            blog = get_object_or_404( Blog.objects, slug = blog )
        else:
            try:
                blog = Blog.objects.get_oldest()
            except Blog.DoesNotExist:
                raise Http404

        request.blog = blog
        return view_func( request, blog = blog, *args, **kwargs )
    _decor.__doc__ = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    return _decor

def post_view( view_func ):
    def _decor( request, blog, *args, **kwargs ):
        if request.user.is_authenticated() and request.user.profile.has_capability_for( BlogRoles.capabilities.edit_post, blog ):
            query_set = Post.objects.for_blog( blog )
        else:
            query_set = Post.published.for_blog( blog )

        post = get_object_or_404( query_set, created_on__year = kwargs.pop( 'year_id' ),
                                        created_on__month     = kwargs.pop( 'month_id' ),
                                        created_on__day       = kwargs.pop( 'day_id' ),
                                        slug            = kwargs.pop( 'post_slug' ) )

        return view_func( request, blog = blog, post = post, *args, **kwargs )
    _decor.__doc__ = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    return _decor
