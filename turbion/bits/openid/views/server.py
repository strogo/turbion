from django import http
from django.contrib import auth
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings

from turbion.bits.profiles import get_profile
from turbion.bits.openid import forms, utils, models
from turbion.bits.utils.urls import uri_reverse
from turbion.bits.utils.decorators import templated, special_titled
from turbion.bits.utils.views import status_redirect

# Maps sreg data fields to Turbion's profile if not equal
SREG_TO_PROFILE_MAP = {
    'fullname': 'full_name',
}

titled = special_titled(section=_("OpenID Server"))

def is_identity_profile(request):
    return get_profile(request).pk == int(settings.TURBION_OPENID_IDENTITY_PROFILE)

def identity_profile_required(view):
    def _decorator(request, *args, **kwargs):
        if not is_identity_profile(request):
            return http.HttpResponseForbidden('Access restricted')
        return view(request, *args, **kwargs)
    return _decorator

def is_trust(url):
    try:
        trust = models.Trust.objects.get(url=url)
        return True
    except models.Trust.DoesNotExist:
        return False

def _render_response(request, openid_response, server=None):
    if not server:
        server = utils.get_server()

    try:
        webresponse = server.encodeResponse(openid_response)
    except EncodingError, why:
        import cgi
        return _render_error(request, cgi.escape(why.response.encodeToKVForm()))

    r = http.HttpResponse(webresponse.body)
    r.status_code = webresponse.code

    for header, value in webresponse.headers.iteritems():
        r[header] = value

    return r

def _render_error(request, message):
    return status_redirect(
        request,
        title=_('Error'),
        section=_("OpenID Server"),
        message=message,
        next='/'
    )

def endpoint(request):
    from openid.server.server import ProtocolError
    server = utils.get_server()

    data = dict(request.REQUEST.items())

    try:
        openid_request = server.decodeRequest(data)
    except ProtocolError, why:
        return _render_error(request, force_unicode(why))

    if openid_request is not None:
        utils._save_request(request, openid_request)
    else:
        openid_request = utils._load_request(request)
        if openid_request is None:
            return http.HttpResponseBadRequest('OpenID consumer request required')

    if openid_request.mode in ["checkid_immediate", "checkid_setup"]:
        if not openid_request.idSelect():
            id_url = settings.TURBION_OPENID_IDENTITY_URL

            # Confirm that this server can actually vouch for that
            # identifier
            if id_url != openid_request.identity:
                # Return an error response
                why = ProtocolError(
                    openid_request.message,
                    "This server cannot verify the URL %r" %
                    (openid_request.identity,)
                )
                return _render_error(request, force_unicode(why))

        # authenticate immediate if possible
        if request.user.is_authenticated()\
            and is_identity_profile(request)\
            and is_trust(openid_request.trust_root):
            openid_response = openid_request.answer(
                True,
                identity=settings.TURBION_OPENID_IDENTITY_URL
            )
            _add_sreg(openid_request, openid_response)
            return _render_response(request, openid_response)

        if openid_request.immediate:
            openid_response = openid_request.answer(
                False,
                identity=settings.TURBION_OPENID_IDENTITY_URL
            )
            return _render_response(request, openid_response)
        else:
            return decide(request, openid_request)
    else:
        openid_response = server.handleRequest(openid_request)
        return _render_response(request, openid_response, server)

@login_required
@identity_profile_required
@templated('turbion/openid/server/decide.html')
@titled(page=_("Trust decision"))
def decide(request, openid_request=None):
    from openid.yadis.discover import DiscoveryFailure
    from openid.fetchers import HTTPFetchingError
    from openid.server.trustroot import verifyReturnTo

    if not openid_request:
        openid_request = utils._load_request(request)

    trust_root = openid_request.trust_root
    return_to = openid_request.return_to

    try:
        # Stringify because template's ifequal can only compare to strings.
        trust_root_valid = verifyReturnTo(trust_root, return_to) \
                           and "Valid" or "Invalid"
    except DiscoveryFailure, err:
        trust_root_valid = "Discovery faild"
    except HTTPFetchingError, err:
        trust_root_valid = "Unreachable"

    allowed = None

    if request.method == "POST"\
                and 'decision' in request.POST:#handle case when consumer request comes with POST
        form = forms.DecideForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data["decision"]

            allowed = decision == "allow"

            if allowed and form.cleaned_data["always"]:
                trust, _ = models.Trust.objects.get_or_create(url=trust_root)

            openid_response = openid_request.answer(
                allowed,
                identity=settings.TURBION_OPENID_IDENTITY_URL
            )
            if allowed:
                _add_sreg(openid_request, openid_response)

            return _render_response(request, openid_response)
    else:
        form = forms.DecideForm()

    return {
        'form': form,
        'trust_root': trust_root,
        'trust_root_valid': trust_root_valid,
    }

def _add_sreg(openid_request, openid_response):
    from openid.extensions import sreg
    from turbion.bits.profiles.models import Profile

    try:
        profile = Profile.objects.get(pk=settings.TURBION_OPENID_IDENTITY_PROFILE)
    except Profile.DoesNotExist:
        return

    sreg_data = {}
    for field in sreg.data_fields.keys():
        try:
            value = getattr(profile, SREG_TO_PROFILE_MAP.get(field, field))
        except AttributeError:
            continue

        if callable(value):
            value = value()

        sreg_data[field] = value

    sreg_req = sreg.SRegRequest.fromOpenIDRequest(openid_request)
    sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
    openid_response.addExtension(sreg_resp)
