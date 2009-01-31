# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.conf import settings

from turbion.core.profiles.models import Profile

def profile_view( view_func ):
    def _decor( request, profile_user, *args, **kwargs ):
        profile = get_object_or_404( Profile, username = profile_user )

        return view_func( request, profile = profile,*args, **kwargs )

    return _decor

def owner_required( view_func ):
    def _check_author(request, profile, *args, **kwargs):
        if request.user.is_authenticated():
            if profile == request.user:
                return view_func(request, profile = profile, *args, **kwargs)
            else:
                return HttpResponseRedirect( request.blog.get_absolute_url() + 'profile/author_required/' )
        else:
            return HttpResponseRedirect( settings.LOGIN_URL )

    _check_author.__doc__ = view_func.__doc__
    _check_author.__dict__ = view_func.__dict__

    return _check_author
