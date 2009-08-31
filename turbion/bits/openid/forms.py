from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from turbion.bits.profiles.models import Profile
from turbion.bits.openid import utils

class OpenidLoginForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [None]

    openid = forms.URLField(label=_("openid"), required=True)

    def __init__(self, request, *args, **kwargs):
        super(OpenidLoginForm, self).__init__(*args, **kwargs)

        self.request = request
        self.created_profile = None

    def clean_openid(self):
        from openid.consumer import discover

        openid_url = self.cleaned_data['openid']

        consumer = utils.get_consumer(self.request.session)
        try:
            self.openid_request = consumer.begin(openid_url)
        except discover.DiscoveryFailure, e:
            raise forms.ValidationError(str(e[0]))

        return openid_url

    def auth_redirect(self, next=None):
        from openid.extensions import sreg

        sreg_request = sreg.SRegRequest(optional=["nickname", "email",])
        self.openid_request.addExtension(sreg_request)

        trust_url, return_to = utils.get_auth_urls(self.request)

        params = {}
        if next or "next" in self.request.REQUEST:
            params['next'] = next or self.request.REQUEST["next"]

        if self.created_profile:
            params['created_profile'] = str(self.created_profile.pk)

        self.openid_request.return_to_args.update(utils.sign_params(params))
        url = self.openid_request.redirectURL(trust_url, return_to)

        return url

class DecideForm(forms.Form):
    decisions = (
        ("allow", _("allow")),
        ("disallow", _("disallow"))
    )

    always = forms.BooleanField(initial=True, label=_('always'), required=False)
    decision = forms.ChoiceField(choices=decisions, initial='allow', label=_('decision'))
