from django.core.urlresolvers import reverse
from django import http
from django.contrib.sites.models import Site
from django.conf import settings

from openid.server.server import CheckIDRequest
from openid.message import Message
from openid.yadis.constants import YADIS_CONTENT_TYPE
from openid.yadis.services import applyFilter
from openid.extensions import sreg

from turbion.utils.testing import RequestFactory

identity_url = "http://%s:%s/id/%s" % (settings.TURBION_TEST_OPENID_SERVER_HOST,
                                       settings.TURBION_TEST_OPENID_SERVER_PORT,
                                       settings.TURBION_TEST_OPENID_SERVER_NICK)

class FakeServer(object):
    def __init__(self, identity_url):
        self.identity_url = identity_url
        self.request = RequestFactory().get("/")

        # Set up the OpenID request we're responding to.
        self.op_endpoint = 'http://%s:%s/openidserver' % (
                                    settings.TURBION_TEST_OPENID_SERVER_HOST,
                                    settings.TURBION_TEST_OPENID_SERVER_PORT
                            )
        message = Message.fromPostArgs({
            'openid.mode': 'checkid_setup',
            'openid.identity': self.identity_url,
            'openid.claimed_id': self.identity_url,
            'openid.return_to': 'http://%s%s' % (Site.objects.get_current().domain,
                                                 reverse("openid_authenticate")),
            'openid.sreg.optional': 'nickname,email',
            'openid.ns': "http://specs.openid.net/auth/2.0",
            'openid.ns.sreg': "http://openid.net/extensions/sreg/1.1"
            })
        self.openid_request = CheckIDRequest.fromMessage(message, self.op_endpoint)

        #if self.openid_request:
        #    self.request.session['openid_request'] = self.openid_request
        #else:
        #    self.request.session['openid_request'] = None

    def _get_server(self):
        from openid.server.server import Server
        from turbion.openid.store import DatabaseStore
        return Server(DatabaseStore(), self.op_endpoint)

    def _process_trust(self, allowed):
        openid_response = self.openid_request.answer(allowed,
                                                     identity=self.identity_url)

        if allowed:
            sreg_data = {
                'fullname': 'Example User',
                'nickname': 'daev',
                'dob': '1987-25-06',
                'email': 'invalid@example.com',
                'gender': 'M',
                'postcode': '127562',
                'country': 'RU',
                'language': 'ru',
                'timezone': 'Europe/Moscow',
                }

            sreg_req = sreg.SRegRequest.fromOpenIDRequest(self.openid_request)
            sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
            openid_response.addExtension(sreg_resp)

        return openid_response

    def get_allow_auth_url(self):
        from openid.server.server import EncodingError

        openid_response = self._process_trust(True)

        s = self._get_server()

        # Encode the response into something that is renderable.
        try:
            webresponse = s.encodeResponse(openid_response)
        except EncodingError, why:
            # If it couldn't be encoded, display an error.
            text = why.response.encodeToKVForm()
            raise ValueError, text

        # Construct the appropriate django framework response.
        r = http.HttpResponse(webresponse.body)
        r.status_code = webresponse.code

        for header, value in webresponse.headers.iteritems():
            r[header] = value
        return r["Location"]

    def get_disallow_auth_url(self):
        openid_response = self._process_trust(False)
