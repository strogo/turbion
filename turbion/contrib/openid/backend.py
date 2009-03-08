from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend

from turbion.core.profiles.models import Profile
from turbion.core.profiles.forms import extract_profile_data
from turbion.contrib.openid import utils

class OpenidBackend(ModelBackend):
    def authenticate(self, request):
        from openid.consumer import consumer as openid_consumer

        consumer, response = utils.complete(request)

        if response.status != openid_consumer.SUCCESS:
            return

        sreg_response = utils.complete_sreg(response) or {}

        data = {
            "nickname": sreg_response.get(
                "nickname",
                Profile.objects.generate_username(response.identity_url)
            ),
            "email": sreg_response.get(
                "email",
                ""
            )
        }

        try:
            profile = Profile.objects.get(openid=response.identity_url)

            # Handle case when we get additional data with SREG
            # for exist profile
            for field, value in data.iteritems():
                if value and not getattr(profile, field):
                    setattr(profile, field, value)

            # profile may be unconfirmed when created
            # while comment/feedback posting
            if not profile.is_confirmed:
                profile.is_confirmed = True
        except Profile.DoesNotExist:
            profile = Profile.objects.create_profile(
                **data
            )
            profile.openid = response.identity_url
            profile.just_created = True

            profile.__dict__.update(
                extract_profile_data(request)
            )

        profile.save()

        return profile
