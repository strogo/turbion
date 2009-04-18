from django.shortcuts import get_object_or_404

from turbion.core.profiles.models import Profile

def profile_view(view_func):
    def _decor(request, profile_id, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=profile_id)

        return view_func(request, profile=profile, *args, **kwargs)

    _decor.__doc__ = view_func.__doc__
    _decor.__dict__ = view_func.__dict__

    return _decor
