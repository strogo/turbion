# -*- coding: utf-8 -*-
import re

from django import forms
from turbion.profiles.models import Profile

user_name_regexp = re.compile("^[\w_]+$")

def check_username(username):
    if user_name_regexp.match(username):
        try:
            Profile.objects.get(username=username)
            raise forms.ValidationError( u"Пользователь с именем %s уже существует. Выберете другое имя." % username )
        except Profile.DoesNotExist:
            pass
    else:
        raise forms.ValidationError( u"Имя пользователя должно содержать только латинские буквы, цифры или _" )

    return  username

def check_email(email):
    try:
        Profile.objects.get(email=email)
        raise forms.ValidationError( u"Данный адрес почты %s уже существует в системе" % email )
    except Profile.DoesNotExist:
        pass

    return email
