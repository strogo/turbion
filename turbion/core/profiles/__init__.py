from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest

def get_profile(obj):
    if isinstance(obj, HttpRequest):
        user = obj.user
    else:
        user = obj

    if isinstance(user, User) and user.__class__.__name__ == "User":
        return user.profile

    if isinstance(user, AnonymousUser):
        from turbion.core.profiles.middleware import AnonymousProfile
        return AnonymousProfile()

    return user
