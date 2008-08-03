# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode

from turbion.profiles import forms
from turbion.profiles.models import Profile
from turbion.profiles.decorators import profile_view, owner_required

from django.shortcuts import *
from pantheon.utils.decorators import titled, templated

@profile_view
@templated( 'turbion/profiles/profile.html' )
@titled( page=u"Главная", section=u"Профайл {{profile.user}}" )
def profile( request, profile ):
    return { "profile" : profile }

@profile_view
@owner_required
@templated( 'turbion/profiles/edit_profile.html' )
@titled( page=u"Редактирование", section=u"Профайл {{profile.user}}" )
def edit_profile( request, profile ):
    if request.POST:
        profile_form = forms.ProfileForm( data = request.POST,
                                          instance = profile )
        if profile_form.is_valid():
            profile_form.save()
    else:
         profile_form = forms.ProfileForm( instance = profile )

    return { "profile_form":  profile_form,
             "profile":       profile }
