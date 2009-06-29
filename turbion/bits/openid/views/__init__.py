from django.views.generic.simple import direct_to_template
from django.conf import settings

from turbion.bits.utils.urls import uri_reverse

def xrds(request):
    from openid.yadis.constants import YADIS_CONTENT_TYPE
    from openid.consumer.discover import OPENID_2_0_TYPE, OPENID_1_0_TYPE
    from openid.server.trustroot import RP_RETURN_TO_URL_TYPE

    return direct_to_template(
        request,
        'turbion/openid/xrds.xml',
        {
            'services': [
                {
                    'types': [OPENID_1_0_TYPE, OPENID_2_0_TYPE],
                    'uri': uri_reverse("turbion_openid_endpoint"),
                    'local_id': settings.TURBION_OPENID_IDENTITY_URL,
                    'delegate': settings.TURBION_OPENID_IDENTITY_URL,
                },
                {
                    'types': [RP_RETURN_TO_URL_TYPE],
                    'uri': uri_reverse('turbion_openid_authenticate'),
                },
            ]
        },
        mimetype=YADIS_CONTENT_TYPE,
    )
