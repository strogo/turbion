from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.core.profiles.models import Profile
from turbion.contrib.openid import utils

class OpenidLoginForm(forms.Form):
    openid = forms.CharField(label=_("openid"), required=True)

    def __init__(self, request, *args, **kwargs):
        super(OpenidLoginForm, self).__init__(*args, **kwargs)

        self.request = request

    def clean_openid(self):
        from openid.consumer import discover

        openid_url = self.cleaned_data['openid']

        consumer = utils.get_consumer(self.request.session)
        errors = []
        try:
            self.openid_request = consumer.begin(openid_url)
        except discover.DiscoveryFailure, e:
            errors.append(str(e[0]))

        if errors:
            raise forms.ValidationError(errors)

        return openid_url

    def auth_redirect(self, target):
        from openid.extensions import sreg

        sreg_request = sreg.SRegRequest(optional=["nickname", "email",])
        self.openid_request.addExtension(sreg_request)

        trust_url, return_to = utils.get_auth_urls(self.request)

        url = self.openid_request.redirectURL(trust_url, return_to)

        return url

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("username", "email")

class DecideForm(forms.Form):
    decisions = (
        ("allow","allow"),
        ("disallow", "disallow")
    )

    always = forms.BooleanField(initial=False)
    decision = forms.ChoiceField(choices=decisions)
