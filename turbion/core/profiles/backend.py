from django.contrib.auth.backends import ModelBackend

from turbion.core.profiles.models import Profile

class OnlyActiveBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = Profile.objects.get(username=username, is_active=True)
            if user.check_password(password):
                return user
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None
