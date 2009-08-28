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
            'nickname', 'email', 'first_name', 'last_name', 'site',
            'name_view', 'filter'
        )

ProfileForm.base_fields.keyOrder = ProfileForm.Meta.fields

def extract_profile_data(request):
    ip = request.META.get('REMOTE_ADDR')
    return {
        'ip': ':' in ip and ip.rsplit(':', 1)[1] or ip
    }

def combine_profile_form_with(form_class, request, field='created_by',\
                              fields=None, filter_field=None, markup_filter_fieled='text_filter'):
    if not get_profile(request).is_trusted():
        from turbion.bits.openid.forms import OpenidLoginForm as BaseForm

        class ProfileForm(form_class, BaseForm):
            nickname  = forms.CharField(required=False, label=_('name'))
            email = forms.EmailField(required=False, label=_('email'),
                                     help_text=_('Only internal usage'))
            site  = forms.URLField(required=False, label=_('site'))

            openid = forms.URLField(required=False, label=_('openid'))

            def __init__(self, initial=None, *args, **kwargs):
                if not initial:
                    initial = {}

                initial.update(get_profile(request).__dict__)
                super(ProfileForm, self).__init__(initial=initial, request=request, *args, **kwargs)

            def get_user(self):
                form_data = dict([(key, value) for key, value in self.cleaned_data.iteritems()\
                                                if key in ['nickname', 'email', 'site', 'openid']])

                profile = get_profile(request)

                openid = form_data.pop('openid', None)

                if not profile.is_authenticated():
                    from django.contrib.auth import login

                    form_data.update(
                        extract_profile_data(request)
                    )

                    #if openid:
                    #    if not form_data.get('nickname', None):
                    #        form_data["nickname"] = openid

                    profile = Profile.objects.create_guest_profile(**form_data)

                    if not openid:
                        profile.backend = '%s.%s' % (
                            ModelBackend.__module__,
                            ModelBackend.__name__
                        )
                        login(request, profile)
                else:
                    profile.__dict__.update(form_data)

                if openid:
                    self.created_profile = profile

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
                if value:
                    return super(ProfileForm, self).clean_openid()
                return value

            def clean(self):
                nickname = self.cleaned_data.get('nickname')
                openid = self.cleaned_data.get('openid')

                if not nickname and not openid:
                    raise forms.ValidationError(_(u'Any of nickname or openid is required.'))

                return self.cleaned_data

        # Remove filter selection for not logged in user
        ProfileForm.base_fields.pop(markup_filter_fieled, None)

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
