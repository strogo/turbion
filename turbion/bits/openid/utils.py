from django.conf import settings

from turbion.bits.utils.urls import uri_reverse
from turbion.bits.profiles.models import Profile
from turbion.bits.openid.models import Association

def _get_store():
    from openid.store.filestore import FileOpenIDStore
    return FileOpenIDStore(settings.TURBION_OPENID_STORE)

def get_consumer(session):
    from openid.consumer import consumer

    return consumer.Consumer(session, _get_store())

def get_server():
    from openid.server import server

    return server.Server(_get_store(), uri_reverse("turbion_openid_endpoint"))

def complete(request):
    data = dict(request.REQUEST.items())

    consumer = get_consumer(request.session)

    trust_url, return_to = get_auth_urls(request)
    response = consumer.complete(data, return_to)

    return consumer, response

def complete_sreg(response):
    from openid.extensions import sreg
    return sreg.SRegResponse.fromSuccessResponse(response)

def get_auth_urls(request=None):
    return settings.TURBION_OPENID_TRUST_URL, uri_reverse('turbion_openid_authenticate')

def _save_request(request, openid_request):
    if openid_request:
        request.session['openid_request'] = openid_request
    else:
        request.session['openid_request'] = None

def _load_request(request):
    return request.session.get('openid_request', None)
