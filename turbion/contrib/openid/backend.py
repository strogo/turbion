from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend

from turbion.core.profiles.models import Profile
from turbion.core.profiles.forms import extract_profile_data
from turbion.contrib.openid import utils

USERNAME_PREFIX = "toi_"

def gen_username(identity_url):
    import md5
    unique = md5.new(identity_url).hexdigest()[:30 - len(USERNAME_PREFIX)]
    return '%s%s' % (USERNAME_PREFIX, unique)

class OpenidBackend(ModelBackend):
    def authenticate(self, request):
        from openid.consumer import consumer as openid_consumer

        consumer, response = utils.complete(request)

        if response.status != openid_consumer.SUCCESS:
            return

        try:
            profile = Profile.objects.get(openid=response.identity_url)
        except Profile.DoesNotExist:
            sreg_response = utils.complete_sreg(response) or {}

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
            profile.openid = response.identity_url
            profile.is_active = True

            profile.__dict__.update(
                extract_profile_data(request)
            )
            profile.save()

        return profile
