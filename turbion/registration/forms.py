# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from turbion.profiles.models import Profile
from turbion.registration import utils

class LoginForm( forms.Form ):
    username = forms.CharField( label = _( 'username' ) )
    password = forms.CharField( label = _( 'password' ), widget = forms.PasswordInput() )

    def clean( self ):
        username = self.cleaned_data[ "username" ]
        password = self.cleaned_data[ "password" ]

        user = authenticate( username=username, password=password )
        if user:pass
            #if not user.is_active:
            #    raise forms.ValidationError( "Ваша учетная запись заблокирована. Обратитесь к администрации")
        else:
            raise forms.ValidationError( _( "Illegal username or password" ) )
        self.cleaned_data[ "user" ] = user
        return self.cleaned_data

class ChangePasswordForm( forms.Form ):
    old_password = forms.CharField( label = _( 'old password' ), widget = forms.PasswordInput() )
    password = forms.CharField( label = _( 'new password' ), widget = forms.PasswordInput() )
    password_confirm = forms.CharField( label = _( 'new password confirm' ), widget = forms.PasswordInput() )

    def __init__(self, request = None, *args, **kwargs ):
        super( ChangePasswordForm, self ).__init__( *args, **kwargs )
        self.request = request

    def clean_old_password(self):
        old_password = self.cleaned_data[ "old_password" ]
        user = self.request.user
        if not user.check_password(old_password):
            raise forms.ValidationError( _( "Wrong old password" ) )

        return old_password

    def clean_password_confirm( self ):
        password = self.cleaned_data[ 'password' ]
        password_confirm = self.cleaned_data[ 'password_confirm' ]

        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError( _( "New password and confirmation don't match" ) )

class ChangeEmailForm( forms.Form ):
    email = forms.EmailField( label = 'e-mail' )

class RestorePasswordForm( forms.Form ):
    email = forms.EmailField( label = 'e-mail' )

    def clean_email( self ):
        email = self.cleaned_data[ 'email' ]
        try:
            user = Profile.objects.get( email = email )
            self.cleaned_data["user"] = user
            return email
        except Profile.DoesNotExist:
            raise forms.ValidationError( _( "Unknown e-mail" ) )

class RegistrationFormBase( object ):
    def clean_email( self ):
        email = self.cleaned_data[ "email" ]
        utils.check_email(email)
        return email

    def clean_username( self ):
        username = self.cleaned_data[ "username" ]
        utils.check_username(username)
        return username

class RegistrationForm( RegistrationFormBase, forms.Form ):
    username = forms.CharField( label = _( 'username' ), required = True )
    email = forms.EmailField( label = 'e-mail', required = True )
    password = forms.CharField( widget = forms.PasswordInput(), label = _( 'password' ), required = True )
    password_confirm = forms.CharField( widget = forms.PasswordInput(), label = _( 'password confirm' ), required = True )

    #captcha = CaptchaField( label = _( 'Check' ), required = True )
    def clean(self):
        self.cleaned_data.pop( "captcha", None )
        del self.cleaned_data[ "password_confirm" ]
        return self.cleaned_data

    def clean_password_confirm( self ):
        password = self.cleaned_data[ 'password' ]
        password_confirm = self.cleaned_data[ 'password_confirm' ]

        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError( _( "Password and confirmation don't match" ) )
