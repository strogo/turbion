from django.conf import settings

from turbion.core.utils.urls import uri_reverse
from turbion.contrib.openid.views import authorization, server

class VerificationMiddleware(object):
    def process_request(self, request):
        from openid.yadis.constants import YADIS_CONTENT_TYPE

        if request.build_absolute_uri() == settings.TURBION_OPENID_TRUST_URL and \
            YADIS_CONTENT_TYPE in request.META.get('HTTP_ACCEPT', ''):
            return authorization.xrds(request)

class YadisMiddleware(object):
    def process_request(self, request):
        from openid.yadis.constants import YADIS_CONTENT_TYPE

        if request.build_absolute_uri() == settings.TURBION_OPENID_IDENTITY_URL and \
            YADIS_CONTENT_TYPE in request.META.get('HTTP_ACCEPT', ''):
            return server.xrds(request)

    def process_response(self, request, response):
        from openid.yadis.constants import YADIS_HEADER_NAME
        
        if response.status_code >= 200 and response.status_code < 300:
            response[YADIS_HEADER_NAME] = uri_reverse('turbion_openid_server_xrds')
        return response
