from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras import SelectDateWidget
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from datetime import date

from turbion.core.profiles import get_profile
from turbion.core.profiles.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'username', 'email', 'first_name', 'last_name', 'site'
            'name_view', 'site_view'
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Profile.objects.get(username=username)
            if user != self.instance:
                raise forms.ValidationError(_('This username already exists'))
        except Profile.DoesNotExist:
            pass

        return username

def extract_profile_data(request):
    return {
        'ip': request.META.get('REMOTE_ADDR'),
        'host': request.META.get('REMOTE_HOST')
    }

USE_OPENID = 'turbion.contrib.openid' in settings.INSTALLED_APPS

def combine_profile_form_with(form_class, request, field='created_by',\
                              fields=None, filter_field=None):
    if not get_profile(request).is_confirmed:
        if USE_OPENID:
            from turbion.contrib.openid.forms import OpenidLoginForm as BaseForm
        else:
            class BaseForm(forms.ModelForm):
                def __init__(self, request, *args, **kwargs):
                    super(BaseForm, self).__init__(*args, **kwargs)

        class UserForm(form_class, BaseForm):
            nickname  = forms.CharField(required=not USE_OPENID, label=_('name'))
            email = forms.EmailField(required=False, label=_('email'),
                                     help_text=_('Only internal usage'))
            site  = forms.URLField(required=False, label=_('site'))

            if USE_OPENID:
                openid = forms.URLField(required=False, label=_('openid'))

            if settings.TURBION_USE_SUPERCAPTCHA:
                from supercaptcha import CaptchaField
                captcha = CaptchaField(label=_('check'))

            def __init__(self, initial=None, *args, **kwargs):
                if not initial:
                    initial = {}

                initial.update(get_profile(request).__dict__)
                super(UserForm, self).__init__(initial=initial, request=request, *args, **kwargs)

            def get_user(self):
                form_data = dict([(key, value) for key, value in self.cleaned_data.iteritems()\
                                                if key in ['nickname', 'email', 'site', 'openid']])

                profile = get_profile(request)

                if not profile.is_authenticated():
                    from django.contrib.auth import login

                    form_data.update(
                        extract_profile_data(request)
                    )

                    profile = None

                    if 'openid' in form_data:
                        try:
                            profile = Profile.objects.get(openid=form_data['openid'])
                        except Profile.DoesNotExist:
                            pass

                    if not profile:
                        profile = Profile.objects.create_guest_profile(**form_data)

                    if not 'openid' in form_data:
                        profile.backend = '%s.%s' % (
                            ModelBackend.__module__,
                            ModelBackend.__name__
                        )
                        login(request, profile)
                else:
                    profile.__dict__.update(form_data)

                profile.save()

                return profile

            def need_auth_redirect(self):
                return self.cleaned_data.get('openid', None) not in (None, '')

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

                initial.update(kwargs.pop('initial', {}))

                super(UserForm, self).__init__(initial=initial, *args, **kwargs)

            def need_auth_redirect(self):
                return False

            def save(self, commit=True):
                obj = super(UserForm, self).save(commit=False)
                setattr(obj, field, get_profile(request))
                if commit:
                    obj.save()

                return obj

    return UserForm
