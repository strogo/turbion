# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse

from django.conf import settings
from turbion.openid import utils
from turbion.registration.forms import RegistrationFormBase

class OpenidLoginForm(forms.Form):
    openid = forms.URLField(label="openid url", required=True)

    def __init__(self, request, **kwargs ):
        super( OpenidLoginForm, self ).__init__( **kwargs )

        self.request = request

    def clean_openid(self):
        from openid.consumer import discover

        openid_url = self.cleaned_data[ 'openid' ]

        consumer = utils.get_consumer(self.request.session)
        errors = []
        try:
            self.openid_request = consumer.begin( openid_url )
        except discover.DiscoveryFailure, e:
            errors.append(str(e[0]))

        if errors:
            raise forms.ValidationError(errors)

        return openid_url

    def auth_redirect(self, target):
        from openid.extensions import sreg

        sreg_request = sreg.SRegRequest( optional=[ "nickname", "email", ])
        self.openid_request.addExtension( sreg_request )

        trust_url, return_to = utils.get_auth_urls(self.request)

        url = self.openid_request.redirectURL( trust_url, return_to )

        return url

class UserInfoForm( forms.Form, RegistrationFormBase ):
    username = forms.CharField( required = True )
    email = forms.EmailField( required = True )
