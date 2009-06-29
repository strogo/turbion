from django.contrib.auth import backends

from turbion.bits.profiles.models import Profile

class ModelBackend(backends.ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = Profile.objects.get(username=username)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
