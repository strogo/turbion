# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django import newforms as forms
from django.newforms.extras import SelectDateWidget

from datetime import date

#from turbion.registration import utils
from turbion.profiles.models import Profile

class ProfileForm( forms.ModelForm ):
    class Meta:
        model = Profile
        fields = ( 'username',
                   'email',
                   'first_name',
                   'last_name',
                   'birth_date',
                   'gender',
                   'city',
                   'country',
                   'biography',
                   'education',
                   'work',
                )

    def clean_username(self):
        username = self.cleaned_data[ 'username' ]
        #if not utils.check_username( username ):
        #    raise forms.ValidationError( "Неправильное имя пользователя" )

        try:
            user = Profile.objects.get( username = username )
            if user != self.instance:
                raise forms.ValidationError( "Данное имя пользователя уже существует" )
        except Profile.DoesNotExist:
            pass

        return username
