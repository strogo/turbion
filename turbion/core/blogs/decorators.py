import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import *

from turbion.core.blogs.models import Post
from turbion.core.utils.decorators import special_titled
from turbion.core.profiles import get_profile

titled = special_titled(section=settings.TURBION_BLOG_NAME)

def post_view(view_func):
    def _decor(request, *args, **kwargs):
        if request.user.is_authenticated():
            query_set = Post.objects.all()
        else:
            query_set = Post.published.all()

            if not get_profile(request).is_trusted():
                query_set = query_set.filter(showing=Post.show_settings.everybody)

        published_on = dict(
            published_on__year=kwargs.pop('year_id'),
            published_on__month=kwargs.pop('month_id'),
            published_on__day=kwargs.pop('day_id'),
        )
        query_set = query_set.filter(slug=kwargs.pop('post_slug'), **published_on)

        post = get_object_or_404(query_set)

        return view_func(request, post=post, *args, **kwargs)
    _decor.__doc__  = view_func.__doc__
    _decor.__dict__ = view_func.__dict__
    _decor.__name__ = view_func.__name__
    return _decor
