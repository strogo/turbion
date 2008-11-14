# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test

from turbion.utils.decorators import special_titled
from django.utils.translation import ugettext_lazy as _

def data_response(func):
    def _decor(reqest, *args, **kwargs):
        pass
    return _decor

def is_superuser(user):
    return user.is_staff and user.is_active and user.is_superuser

superuser_required = user_passes_test(is_superuser)

titled = special_titled(section=_("Turbion dashboard"))
