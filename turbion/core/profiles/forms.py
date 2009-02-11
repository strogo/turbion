# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras import SelectDateWidget

from datetime import date

from turbion.core.utils.captcha.forms import CaptchaField
from turbion.core.profiles import get_profile
from turbion.core.profiles.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'username', 'email', 'first_name', 'last_name', 'birth_date',
            'gender', 'city', 'country', 'biography', 'education', 'work',
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
    return {
        "ip": request.META.get("REMOTE_ADDR"),
        "host": request.META.get("REMOTE_HOST")
    }

def combine_profile_form_with(form_class, request, field="created_by",\
                              need_captcha=True, fields=None,\
                              filter_field=None):
    if not get_profile(request).is_confirmed:
        class UserForm(form_class, forms.ModelForm):
            nickname  = forms.CharField(required=True, label=_ ("name"))
            email = forms.EmailField(required=False, label=_("email"),
                                     help_text=_("Only internal usage"))
            site  = forms.URLField(required=False, label=_("site"))

            if need_captcha:
                captcha = CaptchaField(request=request, required=True, label=_("check"))

            def __init__(self, initial=None, *args, **kwargs ):
                if not initial:
                    initial = {}

                initial.update(get_profile(request).__dict__)
                super(UserForm, self).__init__(initial=initial, *args, **kwargs)

            def get_user(self):
                form_data = dict([(key, value) for key, value in self.cleaned_data.iteritems()\
                                                if key in ['nickname', 'email', 'site']])

                profile = get_profile(request)

                if not profile.is_authenticated():
                    from django.contrib.auth import login
                    from turbion.core.profiles.backend import OnlyActiveBackend

                    form_data.update(
                        extract_profile_data(request)
                    )

                    profile = Profile.objects.create_guest_profile(**form_data)

                    profile.backend = "%s.%s" % (
                        OnlyActiveBackend.__module__,
                        OnlyActiveBackend.__name__
                    )
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
    else:
        class UserForm(form_class):
            def __init__(self, *args, **kwargs):
                if filter_field:
                    initial = {
                        filter_field: get_profile(request).filter
                    }
                else:
                    initial = {}

                initial.update(kwargs.pop("initial", {}))

                super(UserForm, self).__init__(initial=initial, *args, **kwargs)

            def save(self, commit=True):
                obj = super(UserForm, self).save(commit=False)
                setattr(obj, field, get_profile(request))
                if commit:
                    obj.save()

                return obj

    return UserForm
