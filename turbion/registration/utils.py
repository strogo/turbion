# -*- coding: utf-8 -*-
import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from turbion.profiles.models import Profile

user_name_regexp = re.compile("^[\w_]+$")

def check_username(username):
    if user_name_regexp.match(username):
        try:
            Profile.objects.get(username=username)
            raise forms.ValidationError(_("Username %s already exists. Select another username.") % username)
        except Profile.DoesNotExist:
            pass
    else:
        raise forms.ValidationError(_("Username name must content only latin chars and underscores"))

    return  username

def check_email(email):
    try:
        Profile.objects.get(email=email)
        raise forms.ValidationError(_("Email address already exists") % email)
    except Profile.DoesNotExist:
        pass

    return email
