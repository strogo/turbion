from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend

from turbion.core.profiles.models import Profile
from turbion.core.profiles.forms import extract_profile_data
from turbion.contrib.openid import utils
import turbion

class OpenidBackend(ModelBackend):
    def authenticate(self, request):
        from openid.consumer import consumer as openid_consumer

        consumer, response = utils.complete(request)

        if response.status != openid_consumer.SUCCESS:
            turbion.logger.warning("OpenID login fails: %s" % response.status)
            return

        sreg_response = utils.complete_sreg(response) or {}

        data = {
            "nickname": sreg_response.get(
                "nickname",
                response.identity_url
            ),
            "email": sreg_response.get(
                "email",
                ""
            )
        }

        created_profile = request.REQUEST.get('created_profile')
        if created_profile:
            try:
                created_profile = Profile.objects.get(pk=created_profile)
            except Profile.DoesNotExist:
                created_profile = None

        try:
            qs = Profile.objects.filter(openid=response.identity_url)
            if created_profile:
                qs = qs.exclude(pk=created_profile.pk)

            profile = qs.get()
        except Profile.DoesNotExist:
            profile = None

        if not profile:
            if created_profile:
                profile = created_profile

                profile.__dict__.update(
                    data
                )
            else:
                profile = Profile.objects.create_guest_profile(
                    **data
                )
                profile.just_created = True
            profile.openid = response.identity_url

            profile.__dict__.update(
                extract_profile_data(request)
            )
        else:
            if created_profile:
                for rel in Profile._meta.get_all_related_objects():
                    model = rel.model
                    field_name = rel.field.name

                    model._default_manager.filter(**{field_name: created_profile}).update(**{field_name: profile})
                created_profile.delete()

        # profile may be unconfirmed when created
        # while comment/feedback posting
        profile.is_confirmed = True

        profile.save()

        return profile
