# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from turbion.profiles.models import Profile
from turbion.registration.backend import OnlyActiveBackend
from turbion.openid import utils
from turbion.openid.models import Identity

def gen_username(identity_url):
    import md5
    unique = md5.new(identity_url).hexdigest()[:30 - len('toi_')]
    return 'toi_%s' % unique

class OpenidBackend(OnlyActiveBackend):
    def authenticate(self, request):
        from openid.consumer import consumer as openid_consumer

        consumer, response = utils.complete(request)

        if response.status != openid_consumer.SUCCESS:
            return #http.HttpResponseForbidden('Ошибка авторизации: %s' % response.message)

        try:
            connection = Identity.objects.get(url=response.identity_url)
        except Identity.DoesNotExist:
            sreg_response = utils.complete_sreg(response)

            profile = Profile.objects.create_profile(
                                sreg_response.get(
                                    "nickname",
                                    gen_username(response.identity_url)
                                ),
                                sreg_response.get(
                                    "email",
                                    "toi@turbion.turbion"
                                )
                            )
            profile.is_active = True
            profile.save()

            connection = Identity.objects.create(
                user=profile,
                url=response.identity_url
            )

        return connection.user
