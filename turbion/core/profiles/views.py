from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from turbion.core.profiles import forms
from turbion.core.profiles.models import Profile
from turbion.core.profiles.decorators import profile_view, owner_required

from django.shortcuts import *
from turbion.core.utils.decorators import titled, templated

@profile_view
@templated('turbion/profiles/profile.html')
@titled(page=_("Profile"), section="{{profile}}")
def profile(request, profile):
    return {
        "profile": profile
    }

@profile_view
@owner_required
@templated('turbion/profiles/edit.html')
@titled(page=_("Edit"), section=_("Profile {{profile}}"))
def edit_profile(request, profile):
    updated = False
    if request.method == "POST":
        profile_form = forms.ProfileForm(
            data=request.POST,
            instance=profile
        )
        if profile_form.is_valid():
            profile_form.save()
            updated = True
    else:
        profile_form = forms.ProfileForm(instance=profile)

    return {
        "profile_form": profile_form,
        "profile":      profile,
        "just_created": "just_created" in request.GET,
        "updated":      updated,
    }
