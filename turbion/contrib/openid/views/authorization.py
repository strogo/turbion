from django import http
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from turbion.contrib.openid import forms, utils, models, backend

from turbion.core.profiles import get_profile
from turbion.core.utils.decorators import templated, titled

def get_redirect(request):
    redirect = request.REQUEST.get("next", request.META.get("HTTP_REFERER", "/"))

    return redirect

@templated('turbion/openid/login.html')
@titled(page=_("Login"), section=_("OpenID Authorization"))#TODO: add custom_templated with defined `section`
def login(request):
    if request.method == 'POST':
        form = forms.OpenidLoginForm(request, data=request.POST)
        if form.is_valid():
            after_auth_redirect = form.auth_redirect(get_redirect(request))
            return http.HttpResponseRedirect(after_auth_redirect)
    else:
        form = forms.OpenidLoginForm(request.session)
    
    return {
        'form': form,
        'next': get_redirect(request)
    }

def authenticate(request):
    user = auth.authenticate(request=request)

    if not user:
        return http.HttpResponseForbidden(_('Openid authorization error'))

    auth.login(request, user)

    if hasattr(user, "just_created"):
        return http.HttpResponseRedirect(
            reverse("turbion_profile_edit", args=(user.username,)) + "?just_created=1"
        )

    return http.HttpResponseRedirect(request.GET.get('next', '/'))

@login_required
@templated('turbion/openid/collect.html')
@titled(page=_("Information collection"), section=_("OpenID Authorization"))
def collect(request):
    if request.POST:
        user_info_form = forms.UserInfoForm(request.POST, instance=get_profile(request))

        if user_info_form.is_valid():
            user_info_form.save()

            return http.ResponseRedirect(request.GET.get('redirect', '/'))
    else:
        user_info_form = forms.UserInfoForm(instance=request.user)

    return {
        "user_info_form": user_info_form,
        "user_info_form_action": "./",
        "redirect": request.GET.get('redirect', '/')
    }
