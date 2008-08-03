# -*- coding: utf-8 -*-
import re

from django import forms
from turbion.profiles.models import Profile

from turbion.registration.models import ForbiddenName

user_name_regexp = re.compile( "^[A-Za-z0-9_]*$" )

def check_username( username ):
    if user_name_regexp.match( username ):
        try:
            ForbiddenName.objects.get( name = username )
            raise forms.ValidationError( u"Пользователь с именем %s уже существует. Выберете другое имя." % username )
        except ForbiddenName.DoesNotExist:
            pass

        try:
            Profile.objects.get( username = username )
            raise forms.ValidationError( u"Пользователь с именем %s уже существует. Выберете другое имя." % username )
        except Profile.DoesNotExist:
            pass
    else:
        raise forms.ValidationError( u"Имя пользователя должно содержать только латинские буквы, цифры или _" )

    return  username

def check_email( email ):
    try:
        Profile.objects.get( email = email )
        raise forms.ValidationError( u"Данный адрес почты %s уже существует в системе" % email )
    except Profile.DoesNotExist:
        pass

    return email
