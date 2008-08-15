# -*- coding: utf-8 -*-
from django.contrib import auth
from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.conf import settings

from turbion.registration import forms
from turbion.registration.models import Offer
from turbion.registration import mail
from turbion.profiles.models import Profile

from turbion.utils.decorators import templated, special_titled
from turbion.utils.views import status_redirect

SECTION = _("Registration")
titled = special_titled(section=SECTION)

@templated('turbion/registration/restore_password_request.html')
@titled(page=_("Password restore request"))
def restore_password_request(request):
    if request.POST:
        form = forms.RestorePasswordForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            code = Offer.objects.create(user=user,
                                        type="password_restore")

            mail.RestorePasswordRequestMessage(code.user.email, {"code": code.code}).send()
            return status_redirect(request,
                              title=_("Password request notification"),
                              section=SECTION,
                              message=_("Check your e-mail inbox for notification message"),
                              next=u"/",
                )
    else:
        form = forms.RestorePasswordForm()
    action = "./"
    return { "form": form,
            "action":action }

def restore_password(request):
    code = request.GET.get("code", None)

    if code:
        restore_request = get_object_or_404( Offer, code = code )
        user = restore_request.user

        new_password = Profile.objects.make_random_password()

        user.set_password(new_password)
        user.save()

        mail.RestorePasswordMessage( restore_request.user.email, { "user":user,
                                                                   "new_password":new_password} ).send()

        restore_request.delete()

        return status_redirect(request,
                          title= _( "Notification" ),
                          section=SECTION,
                          message=_( "Check your e-mail inbox for new creditionals" ),
                          next= "/",
                )#template="turbion/registration/info.html"

    raise http.Http404

@templated('turbion/registration/change_email.html')
@titled(page=_("E-mail change"))
@login_required
def change_email(request):
    if request.method == 'POST':
        form = forms.ChangeEmailForm(data=request.POST)
        if form.is_valid():
            code = Offer.objects.create(user=request.user,
                                       type="email_change",
                                       data=form.cleaned_data["email"])

            mail.ChangeEmailMessage(code.user.email, {"code": code}).send()
            return status_redirect(request,
                              title= _( "E-mail change notification" ),
                              section=SECTION,
                              message= _( "Check your e-mail inbox for instructions" ),
                              next= "/"
                        )
    else:
        form = forms.ChangeEmailForm()

    return {"form": form}


@templated('turbion/registration/change_email.html')
@titled(page=_("E-mail confirmation"))
@login_required
def change_email_confirm(request):
    code = request.GET.get('code', None)
    if code:
        code = get_object_or_404(Offer, user=request.user, type="email_change", code=code)
        code.user.email = code.data
        code.user.save()

        code.delete()
        return status_redirect(request,
                          title= _( "Notification" ),
                          section= SECTION,
                          message= _( "Your new e-mail has been confirmed" ),
                          next= "/"
                    )
    raise http.Http404

@templated('turbion/registration/change_password.html')
@titled(page=_("Password change"))
@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request=request, data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()

            return status_redirect(request,
                              title= _( "Password has changed" ),
                              section = SECTION,
                              message= _( "Now you can sing-in with your new password" ),
                              next = request.GET.get( 'redirect', '/' )
                )
    else:
        form = forms.ChangePasswordForm()

    return {"change_password_form": form}

@templated('turbion/registration/registration.html')
@titled(page=_( "Information collection"))
def registration(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = Profile.objects.create_user(**data)
            user.is_active = False
            user.save()

            code = Offer.objects.create(user=user)
            mail.RegistrationConfirmMessage(user.email, {"user": user, "code": code}).send()

            return status_redirect(request,
                              title= _( "Registration notification" ),
                              section=SECTION,
                              message= _( "Check your e-mail inbox for instructions" ),
                              next= "/"
                            )
    else:
        form = forms.RegistrationForm()

    return {"registration_form": form }

def registration_confirm(request):
    code = request.GET.get('code', None)
    if code:
        code = get_object_or_404(Offer, code=code)
        code.user.is_active = True
        code.user.save()
        code.delete()

        return status_redirect(request,
                        title=_("Registration finished"),
                        section=SECTION,
                        message= _("Now you can sing-in with your account"),
                        next=settings.LOGIN_URL
                    )

    raise http.Http404
