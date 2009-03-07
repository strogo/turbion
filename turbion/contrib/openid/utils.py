from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from turbion.core.utils.urls import uri_reverse
from turbion.core.profiles.models import Profile
from turbion.contrib.openid.models import Association

def get_consumer(session):
    from openid.consumer import consumer
    from turbion.openid.store import DatabaseStore

    return consumer.Consumer(session, DatabaseStore(Association.origins.consumer))

def get_server():
    from openid.server import server
    from turbion.openid.store import DatabaseStore

    return server.Server(
        DatabaseStore(Association.origins.server),
        uri_reverse("turbion_openid_endpoint")
    )

def complete(request):
    data = dict(request.GET.items())
    if request.method=="POST":
        data.update(dict(request.POST.items()))

    consumer = get_consumer(request.session)

    trust_url, return_to = get_auth_urls(request)
    response = consumer.complete(data, return_to)

    return consumer, response

def complete_sreg(response):
    from openid.extensions import sreg
    return sreg.SRegResponse.fromSuccessResponse(response)

def get_auth_urls(request):
    site_url =  "http://%s" % Site.objects.get_current().domain
    trust_url = getattr(settings, "TURBION_OPENID_TRUST_URL", (site_url + '/'))
    return_to = site_url + reverse('turbion_openid_authenticate')

    return trust_url, return_to

def _save_request(request, openid_request):
    if openid_request:
        request.session['openid_request'] = openid_request
    else:
        request.session['openid_request'] = None

def _load_request(request):
    return request.session.get('openid_request', None)
