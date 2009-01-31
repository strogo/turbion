# -*- coding: utf-8 -*-
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode

from turbion.core.profiles import get_profile

def has_capability(cap=None, set=None, instance=None, all=True):
    assert(cap is not None or set is not None)

    def _wrapper(func):
        @login_required
        def _decorator(request, *args, **kwargs):
            if instance:
                if callable(instance):
                    obj = obj_name(request, *args, **kwargs)
                elif isinstance(instance, basestring):
                    obj = kwargs[instance]
                else:
                    obj = instance
            else:
                obj = None

            if get_profile(request).has_capability(cap=cap, set=set, instance=obj, all=all):
                return func(request, *args, **kwargs)
            else:
                return http.HttpResponseRedirect(
                    reverse("turbion_no_capability") + "?" + urlencode({"from": request.path}, doseq=True)
                )

        _decorator.__doc__ = func.__doc__
        _decorator.__dict__ = func.__dict__
        _decorator.perm = perm
        return _decorator
    return _wrapper
