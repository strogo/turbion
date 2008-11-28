# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from turbion.profiles.models import Profile
from turbion.registration import utils

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='e-mail')

class RestorePasswordForm(forms.Form):
    email = forms.EmailField(label='e-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Profile.objects.get(email=email)
            self.cleaned_data["user"] = user
            return email
        except Profile.DoesNotExist:
            raise forms.ValidationError(_("Unknown e-mail"))

class RegistrationFormBase(object):
    def clean_email(self):
        email = self.cleaned_data["email"]
        utils.check_email(email)
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        utils.check_username(username)
        return username

class CreateProfileForm(RegistrationFormBase, forms.Form):
    username = forms.CharField(label=_('username'), required=True)
    email = forms.EmailField(label='e-mail', required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label=_('password'), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label=_('password confirm'), required=True)

    #captcha = CaptchaField(label=_('Check'), required=True)
    def clean(self):
        if "captcha" in self.cleaned_data:
            del self.cleaned_data["captcha"]

        if "new_password2" in self.cleaned_data:
            del self.cleaned_data["new_password2"]
            
        return self.cleaned_data

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']

        if new_password1 == new_password2:
            return new_password2
        raise forms.ValidationError(_("Password and confirmation don't match"))

    def save(self):
        return self.create_profile(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["new_password1"]
        )

    def create_profile(self, username, email, password):
        profile = Profile.objects.create_user(username, email, password)

        return profile

RegistrationForm = CreateProfileForm

class RegistrationConfirmForm(forms.Form):
    code = forms.CharField(required=True)

    def clean_code(self):
        from turbion.registration.models import Offer
        code = self.cleaned_data["code"]

        try:
            code = Offer.objects.get(code=code)
        except OfferDoesNotExist:
            raise forms.ValidationError(_("Registration offer does not exist"))

        return code
