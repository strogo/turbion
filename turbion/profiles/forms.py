# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras import SelectDateWidget

from datetime import date

from pantheon.supernovaforms.fields import CaptchaField

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
        username = self.cleaned_data['username']
        try:
            user = Profile.objects.get(username=username)
            if user != self.instance:
                raise forms.ValidationError(_("This username already exists"))
        except Profile.DoesNotExist:
            pass

        return username

def extract_profile_data(request):
    return {"ip": request.META.get("REMOTE_ADDR")}

def combine_profile_form_with(form_class, request, field="created_by", need_captcha=True):
    if not request.user.is_authenticated():
        class UserForm(form_class, forms.ModelForm):
            nickname  = forms.CharField(required=True, label=_ ("name"))
            email = forms.EmailField(required=False, label=_("email"))
            site  = forms.URLField(required=False, label=_("site"))

            if need_captcha:
                captcha = CaptchaField(required=True, label=_("check"))

            def __init__(self, initial=None, *args, **kwargs ):
                if not initial:
                    initial = {}
                if request.user.is_authenticated():
                    initial.update(request.user.__dict__)
                super(UserForm, self).__init__(initial=initial, *args, **kwargs)

            def get_user(self):
                form_data = dict([(key, value) for key, value in self.cleaned_data.iteritems()\
                                                if key in self.fields.keys()])

                profile = request.user

                if not profile.is_authenticated():
                    from django.contrib.auth import login
                    profile = Profile.objects.create_guest_profile(**form_data)
                    login(request, profile)
                else:
                    profile.__dict__.update(form_data)

                profile.save()

                return profile

            def save(self, commit=True):
                obj = super(UserForm, self).save(False)

                user = self.get_user()

                setattr(obj, field, user)
                if commit:
                    obj.save()

                return obj

        return UserForm

    form_save = form_class.save

    def save(self, commit=True):
        obj = form_save(self, commit=False)
        setattr(obj, field, request.user)
        if commit:
            obj.save()

        return obj

    form_class.save = save

    return form_class
