# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import *

import re

from turbion.blogs.models import Blog, Post, BlogRoles

from turbion.utils.decorators import special_titled

titled = special_titled(section=u"{{blog.name}}")

def blog_view(view_func):
    """
    Picks up blog slug and `converts` it into blog object
    """
    def _decor(request, blog=None, *args, **kwargs):
        if blog is not None:
            blog = get_object_or_404(Blog.objects, slug=blog)
        else:
            try:
                blog = Blog.objects.get_oldest()
            except Blog.DoesNotExist:
                raise Http404

        request.blog = blog
        return view_func(request, blog=blog, *args, **kwargs)
    _decor.__doc__  = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    _decor.__name__ = view_func.__name__
    return _decor

def post_view(view_func):
    def _decor(request, blog, *args, **kwargs):
        if request.user.is_authenticated() and request.user.has_capability_for(BlogRoles.capabilities.edit_post, blog):
            query_set = Post.objects.for_blog(blog)
        else:
            query_set = Post.published.for_blog(blog)

            if not request.user.is_authenticated_confirmed():
                query_set = query_set.filter(showing=Post.show_settings.everybody)

        published_on = dict(
            published_on__year=kwargs.pop('year_id'),
            published_on__month=kwargs.pop('month_id'),
            published_on__day=kwargs.pop('day_id'),
        )
        query_set = query_set.filter(slug=kwargs.pop('post_slug'), **published_on)

        post = get_object_or_404(query_set)

        return view_func(request, blog=blog, post=post, *args, **kwargs)
    _decor.__doc__  = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    _decor.__name__ = view_func.__name__
    return _decor
