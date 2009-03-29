from django import http
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str

from turbion.contrib.openid import forms, utils, models, backend

from turbion.core.profiles import get_profile
from turbion.core.utils.decorators import templated, special_titled

titled = special_titled(section=_("OpenID Authorization"))

def get_redirect(request):
    redirect = request.REQUEST.get("next", request.META.get("HTTP_REFERER", "/"))

    return redirect

@templated('turbion/openid/login.html')
@titled(page=_("Login"))
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

@templated('turbion/openid/result.html')
@titled(page=_("Result"))
def authenticate(request):
    user = auth.authenticate(request=request)

    if not user:
        return {
            'success': False,
            'message': _('Openid authentication error')
        }

    auth.login(request, user)

    if hasattr(user, "just_created"):
        return http.HttpResponseRedirect(
            reverse("turbion_profile_edit", args=(user.pk,)) + "?just_created=1"
        )

    return http.HttpResponseRedirect(request.GET.get('next', '/'))
