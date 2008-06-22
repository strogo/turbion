# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007 Alexander Koshelev (daevaorn@gmail.com)
from django.contrib import auth
from django import http
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from turbion.registration import forms
from turbion.registration.models import Code
from turbion.registration import mail

from pantheon.utils.decorators import render_to, special_title_bits
from pantheon.utils.views import info_page

SECTION = _( "Registration" )
title_bits = special_title_bits( section = SECTION )

@title_bits( page= _( "Login" ) )
@render_to( 'registration/login.html' )
def login( request ):
    if request.method == 'POST':
        login_form = forms.LoginForm( request.POST )
        if login_form.is_valid():
            user = login_form.cleaned_data[ "user" ]
            auth.login( request, user )

            return http.HttpResponseRedirect( request.GET.get( 'redirect', user.get_profile().get_absolute_url() ) )
    else:
        login_form = forms.LoginForm()
        
    login_form_action = './?redirect=' + request.GET.get( 'redirect', '/' ) 

    return { "login_form": login_form,
            "login_form_action":login_form_action }

@login_required
def logout( request ):
    if request.method=='POST':
        auth.logout( request )
    return  http.HttpResponseRedirect( request.GET.get( 'redirect', '/' ) )


@title_bits( page = _("Password restore request") )#u"Запрос востановления пароля" 
@render_to( 'registration/restore_password_request.html' )
def restore_password_request( request ):
    if request.POST:
        form = forms.RestorePasswordForm( data = request.POST )
        if form.is_valid():
            user = form.cleaned_data[ 'user' ]
            code = Code.objects.create( user = user,
                                        type = "password_restore" )
                
            mail.RestorePasswordRequestMessage( code.user.email, { "code" :code.code } ).send()
            return info_page( request,
                              title=_( "Password request notification" ),
                              section=SECTION,
                              message=_("Check your e-mail inbox for notification message"),
                              next=u"/",
                              template="registration/info.html" )
    else:
        form = forms.RestorePasswordForm()
    action = "./"
    return { "form": form,
            "action":action }

def restore_password( request ):
    code = request.GET.get( "code", None )
    
    if code:
        restore_request = get_object_or_404( Code, code = code )
        user = restore_request.user
        
        new_password = User.objects.make_random_password()
        
        user.set_password( new_password )
        user.save()
        
        mail.RestorePasswordMessage( restore_request.user.email, { "user":user,
                                                                   "new_password":new_password} ).send()
        
        restore_request.delete()
        
        return info_page( request,
                          title= _( "Notification" ),
                          section=SECTION,
                          message=_( "Check your e-mail inbox for new creditionals" ),
                          next= "/",
                          template="registration/info.html" )
    
    raise http.Http404

@title_bits( page = _( "E-mail change" ) )#u"Изменение почтового адреса"
@render_to( 'registration/change_email.html' )
@login_required
def change_email( request ):
    if request.method == 'POST':
        form = forms.ChangeEmailForm( data = request.POST )
        if form.is_valid():
            code = Code.objects.create( user = request.user,
                                        type = "email_change",
                                        data = form.cleaned_data["email"] )
            
            mail.ChangeEmailMessage( code.user.email, { "code" : code } ).send()
            return info_page( request,
                              title= _( "E-mail change notification" ),
                              section=SECTION,
                              message= _( "Check your e-mail inbox for instructions" ),
                              next= "/",
                              template="registration/info.html" )
    else:
        form = forms.ChangeEmailForm()
    
    return { "form" : form }

@title_bits( page = _( "E-mail confirmation" ) )#u"Подтверждение почтового адреса"
@render_to( 'registration/change_email.html' )
@login_required
def change_email_confirm( request ):
    code = request.GET.get( 'code', None )
    if code:
        code = get_object_or_404( Code, user = request.user, type = "email_change", code = code )
        code.user.email = code.data
        code.user.save()
            
        code.delete()
        return info_page( request,
                          title= _( "Notification" ),
                          section= SECTION,
                          message= _( "Your new e-mail has been confirmed" ),
                          next= "/",
                          template="registration/info.html" )
    raise http.Http404

@title_bits( page = _( "Password change" ) )#u"Изменение пароля"
@render_to( 'registration/change_password.html' )
@login_required
def change_password( request ):
    if request.method == 'POST':
        form = forms.ChangePasswordForm( request = request, data = request.POST )
        if form.is_valid():
            request.user.set_password( form.cleaned_data[ "password" ] )
            request.user.save()
            
            return info_page( request,
                              title= _( "Password has changed" ),
                              section = SECTION,
                              message= _( "Now you can sing-in with your new password" ),
                              next = request.GET.get( 'redirect', '/' ),
                              template="registration/info.html" )
    else:
        form = forms.ChangePasswordForm()
    
    return { "change_password_form": form }

@render_to( 'registration/registration.html' )
@title_bits( page= _( "Information collection" ) )#u"Сбор сведений"
def registration( request ):
    if request.method == 'POST':
        form = forms.RegistrationForm( data = request.POST )
        if form.is_valid():
            data = form.cleaned_data
            
            user = User.objects.create_user( **data )
            user.is_active = False
            user.save()
            
            code = Code.objects.create( user = user )
            mail.RegistrationConfirmMessage( user.email, { "user" : user, "code":code } ).send()
            
            return info_page( request,
                              title= _( "Registration notification" ),
                              section=SECTION,
                              message= _( "Check your e-mail inbox for instructions" ),
                              next= "/",
                              template="registration/info.html" )
    else:
        form = forms.RegistrationForm()
    registration_action = './'

    return { "registration_form": form,
             "registration_action": registration_action }

def registration_confirm( request ):
    code = request.GET.get( 'code', None )
    if code:        
        code = get_object_or_404( Code, code = code )
        code.user.is_active = True
        code.user.save()
        code.delete()

        return info_page( request,
                          title= _( "Registration finished" ),
                          section = SECTION,
                          message= _( "Now you can sing-in with your account" ),
                          next= reverse( "turbion.registration.views.login" ),
                          template="registration/info.html" )

    raise http.Http404