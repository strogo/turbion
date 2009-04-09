import cgi

from django import http
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from turbion.contrib.openid import forms, utils, models
from turbion.core.utils.urls import uri_reverse
from turbion.core.utils.decorators import templated, titled

# Maps sreg data fields to Turbion's profile if not equal
SREG_TO_PROFILE_MAP = {
    'fullname': 'full_name',
}

@templated('turbion/openid/server/endpoint.html')
@titled(page=_("Endpoint"), section=_("OpenID Server"))
def endpoint(request):
    from openid.server.server import ProtocolError
    server = utils.get_server()

    data = dict(request.GET.items())
    if request.method == "POST":
        data.update(dict(request.POST.items()))

    try:
        openid_request = server.decodeRequest(data)
    except ProtocolError, why:
        return {
            'error': str(why)
        }

    if openid_request is None:
        return {}

    if openid_request.mode in ["checkid_immediate", "checkid_setup"]:
        return _check_id(request, openid_request)
    else:
        openid_response = server.handleRequest(openid_request)
        return _render_response(request, openid_response)

def _check_id(request, openid_request):
    if not openid_request.idSelect():
        id_url = getViewURL(request, idPage)

        # Confirm that this server can actually vouch for that
        # identifier
        if id_url != openid_request.identity:
            # Return an error response
            error_response = ProtocolError(
                openid_request.message,
                "This server cannot verify the URL %r" %
                (openid_request.identity,))

            return displayResponse(request, error_response)

    if openid_request.immediate:
        #FIXME: handle this type of request
        openid_response = openid_request.answer(False)
        return _render_response(request, openid_response)
    else:
        utils._save_request(request, openid_request)
        return decide(request, openid_request)

def _render_response(request, openid_request):
    server = utils.get_server()

    try:
        webresponse = server.encodeResponse(openid_response)
    except EncodingError, why:
        text = why.response.encodeToKVForm()
        return direct_to_template(
            request,
            "turbion/openid/server/error.html",
            {'error': cgi.escape(text)}
        )

    r = http.HttpResponse(webresponse.body)
    r.status_code = webresponse.code

    for header, value in webresponse.headers.iteritems():
        r[header] = value

    return r

@templated('turbion/openid/server/decide.html')
@titled(page=u"Trust decision", section=u"OpenID Server")
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
        trust_root_valid = "DISCOVERY_FAILED"
    except HTTPFetchingError, err:
        trust_root_valid = "Unreachable"

    if request.method=="POST":
        form = forms.DecideForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data["decision"]

            allowed = decision == "allow"

            openid_response = openid_request.answer(
                                allowed,
                                identity=response_identity
                            )

            if allowed:
                if form.cleaned_data["allways"]:
                    Trust.objects.get_or_create(url=identity_url)

                _add_sreg(request, openid_response)

            return _render_response(request, openid_response)
    else:
        form = forms.DecideForm()

    return {
        'form': form,
        'trust_root': trust_root,
        'trust_handler_url':getViewURL(request, processTrustResult),
        'trust_root_valid': trust_root_valid,
    }

def _add_sreg(request, openid_response):
    from openid.extension import sreg
    from turbion.core.profiles.models import Profile

    try:
        profile = Profile.objects.get(pk=settings.TURBION_OPENID_IDENTITY_PROFILE)
    except Profile.DoesNotExist:
        return

    sreg_data = {}
    for field in sreg.data_fields.keys():
        try:
            value = getattr(profile, SREG_TO_PROFILE_MAP.get(field, field))
        except AtteibuteError:
            continue

        if callable(value):
            value = value()

        data[field] = value

    sreg_req = sreg.SRegRequest.fromOpenIDRequest(openid_request)
    sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
    openid_response.addExtension(sreg_resp)

def xrds(request):
    from openid.yadis.constants import YADIS_CONTENT_TYPE
    from openid.consumer.discover import OPENID_IDP_2_0_TYPE

    return direct_to_template(
        request,
        'turbion/openid/server/xrds.xml',
        {
            'type_uri': OPENID_IDP_2_0_TYPE,
            'endpoint_url': uri_reverse("turbion_openid_endpoint"),
        },
        mimetype=YADIS_CONTENT_TYPE,
    )
