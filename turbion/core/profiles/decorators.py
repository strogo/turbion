from django.core.urlresolvers import reverse
from django import http
from django.shortcuts import *
from django.conf import settings

from turbion.core.profiles.models import Profile
from turbion.core.profiles import get_profile

def profile_view(view_func):
    def _decor(request, profile_user, *args, **kwargs):
        profile = get_object_or_404(Profile, username=profile_user)

        return view_func(request, profile=profile, *args, **kwargs)

    _decor.__doc__ = view_func.__doc__
    _decor.__dict__ = view_func.__dict__

    return _decor

def owner_required(view_func):
    def _check_author(request, profile, *args, **kwargs):
        if request.user.is_authenticated():
            if profile == get_profile(request):
                return view_func(request, profile=profile, *args, **kwargs)
            else:
                return http.HttpResponseForbidden("Profile owner required")
        else:
            return http.HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    _check_author.__doc__ = view_func.__doc__
    _check_author.__dict__ = view_func.__dict__

    return _check_author
