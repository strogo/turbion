from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend
from django.db import IntegrityError

from turbion.bits.profiles.models import Profile
from turbion.bits.profiles.forms import extract_profile_data
from turbion.bits.openid import utils
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

        # Getting profile created by comment post.
        # We must associate this identity with it
        created_profile = utils.extract_params(request.GET).get('created_profile')
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

        if profile:# user already exists
            if created_profile:
                self._merge_profiles(created_profile, profile)
        else:# completely new user
            if created_profile:# but with already created profile
                profile = created_profile

                profile.__dict__.update(
                    data
                )
            else:# not profile yet. create it
                profile = Profile.objects.create_guest_profile(
                    **data
                )
                profile.just_created = True
                profile.__dict__.update(
                    extract_profile_data(request)
                )

            profile.openid = response.identity_url
            profile.save()

        return profile

    def _merge_profiles(self, created_profile, old_profile):
        for rel in Profile._meta.get_all_related_objects():
            model = rel.model
            field_name = rel.field.name

            try:
                model._default_manager.filter(**{field_name: created_profile})\
                                        .update(**{field_name: old_profile})
            except IntegrityError:
                # May produce error with duplicate key
                # For example when user auths second time and get another
                # watchlist subscription to same post
                pass
        created_profile.delete()
