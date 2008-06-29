# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007, 2008 Alexander Koshelev (daevaorn@gmail.com)
from openid.consumer import consumer as openid_consumer

from django import http
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from turbion.openid import forms, utils, models

from pantheon.utils.decorators import *

def post_redirect( request ):
    redirect = request.GET.get( "redirect", None ) or request.META.get( "HTTP_REFERER", "/" )

    return redirect

@title_bits( page=u"Вход", section=u"Авторизация OpenID" )
@render_to( 'openid/login.html' )
def login(request):
    if request.method == 'POST':
        form = forms.OpenidLoginForm( request, data = request.POST)
        if form.is_valid():
            after_auth_redirect = form.auth_redirect(post_redirect(request))
            return http.HttpResponseRedirect( after_auth_redirect )
    else:
        form = forms.OpenidLoginForm( request.session )
    return {'form': form, 'redirect': post_redirect(request)}

def authenticate(request):
    consumer, response = utils.complete( request )

    if response.status != openid_consumer.SUCCESS:
        return http.HttpResponseForbidden('Ошибка авторизации')

    try:
        connection = models.Identity.objects.get( url = response.identity_url )
    except models.Identity.DoesNotExist:
        sreg_response = utils.complete_sreg( response )

        request.session[ "openid_data" ] = { "response" : response, "sreg_response" : sreg_response }
        return http.HttpResponseRedirect( reverse( "turbion.openid.views.collect" ) )

    #user = auth.authenticate( request=request )
    #if not user:
    #    return HttpResponseForbidden('Ошибка авторизации')
    auth.login(request, connection.user)
    return http.HttpResponseRedirect(request.GET.get('redirect', '/'))

@title_bits( page=u"Сбор сведений", section=u"Авторизация OpenID" )
@render_to( 'openid/collect.html' )
def collect(request):
    if "openid_data" in request.session:
        response = request.session[ "openid_data" ][ "reponse" ]
        sreg_response =  request.session[ "openid_data" ][ "sreg_response" ]

        if request.POST:
            user_info_form = forms.UserInfoForm( request.POST )
        else:
            user_info_form = forms.UserInfoForm( data = { "username": sreg_response.get("nickname",""),
                                                          "email"  : sreg_response.get("email","") } )

        if user_info_form.is_valid():
            username = user_info_form.cleaned_data[ "nickname" ]
            email = user_info_form.cleaned_data[ "email" ]

            connection = utils.create_user( username, email, response )
            auth.login(request, connection.user)
            request.session.delete( "openid_data" )
            return http.ResponseRedirect( request.GET.get( 'redirect', '/' ) )

        return { "user_info_form" : user_info_form,
                 "user_info_form_action" : "./",
                 "redirect" : request.GET.get('redirect', '/') }
    raise http.Http404