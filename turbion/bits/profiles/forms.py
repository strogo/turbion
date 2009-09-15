from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras import SelectDateWidget
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from datetime import date

from turbion.bits.profiles import get_profile
from turbion.bits.profiles.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'nickname', 'email', 'first_name', 'last_name',
            'name_view', 'filter'
        )

ProfileForm.base_fields.keyOrder = ProfileForm.Meta.fields

def extract_profile_data(request):
    ip = request.META.get('REMOTE_ADDR')
    return {
        'ip': ':' in ip and ip.rsplit(':', 1)[1] or ip
    }

def combine_profile_form_with(form_class, request, field='created_by',\
                              fields=None, filter_field='text_filter'):
    if not get_profile(request).is_authenticated():
        from turbion.bits.openid.forms import OpenidLoginForm as BaseForm

        class ProfileForm(form_class, BaseForm):
            openid = forms.CharField(label=_('Name or OpenID'), required=True)

            def __init__(self, initial=None, *args, **kwargs):
                if initial is None:
                    initial = {}

                initial.update(get_profile(request).__dict__)
                super(ProfileForm, self).__init__(
                    initial=initial, request=request, *args, **kwargs
                )

                self.valid_openid = False

            def get_user(self):
                from django.contrib.auth import login
                form_data = {'nickname': self.cleaned_data['openid']}
                form_data.update(extract_profile_data(request))

                profile = get_profile(request)

                if not profile.is_authenticated():
                    profile = Profile.objects.create_guest_profile(**form_data)

                    if not self.valid_openid:
                        profile.backend = '%s.%s' % (
                            ModelBackend.__module__,
                            ModelBackend.__name__
                        )
                        login(request, profile)
                    else:
                        self.created_profile = profile
                else:
                    profile.__dict__.update(form_data)

                profile.save()

                return profile

            def need_auth_redirect(self):
                return self.cleaned_data.get('openid', None) not in (None, '')

            def save(self, commit=True):
                obj = super(ProfileForm, self).save(False)

                user = self.get_user()

                setattr(obj, field, user)
                if commit:
                    obj.save()

                return obj

            def clean_openid(self):
                value = self.cleaned_data["openid"]
                if value.startswith('http://'):
                    try:
                        value = super(ProfileForm, self).clean_openid()
                        self.valid_openid = True
                    except forms.ValidationError:
                        pass
                return value

        return ProfileForm
    else:
        class ProfileForm(form_class):
            def __init__(self, *args, **kwargs):
                if filter_field:
                    initial = {
                        filter_field: get_profile(request).filter
                    }
                else:
                    initial = {}

                initial.update(kwargs.pop('initial', {}))

                super(ProfileForm, self).__init__(initial=initial, *args, **kwargs)

            def need_auth_redirect(self):
                return False

            def save(self, commit=True):
                obj = super(ProfileForm, self).save(commit=False)
                setattr(obj, field, get_profile(request))
                if commit:
                    obj.save()

                return obj

    return ProfileForm
