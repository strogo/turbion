from django.conf import settings

from turbion.bits.utils.urls import uri_reverse
from turbion.bits.openid import views

class YadisMiddleware(object):
    def process_request(self, request):
        from openid.yadis.constants import YADIS_CONTENT_TYPE

        if YADIS_CONTENT_TYPE in request.META.get('HTTP_ACCEPT', ''):
            if request.build_absolute_uri() in (
                settings.TURBION_OPENID_TRUST_URL,
                settings.TURBION_OPENID_IDENTITY_URL
            ):
                return views.xrds(request)

    def process_response(self, request, response):
        from openid.yadis.constants import YADIS_HEADER_NAME

        if request.build_absolute_uri() == settings.TURBION_OPENID_IDENTITY_URL and \
            response.status_code >= 200 and response.status_code < 300:
            response[YADIS_HEADER_NAME] = uri_reverse('turbion_openid_xrds')

        return response
