from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend, ImproperlyConfigured

from turbion.bits.profiles.models import Profile

class AnonymousProfile(AnonymousUser):
    nickname = None
    ip = None
    trusted = False
    name_view = None
    openid = None

    def is_trusted(self):
        return self.trusted

def get_profile(request):
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        if user and not isinstance(user, Profile):
            user = user.profile
        else:
            user = AnonymousProfile()
    except (KeyError, Profile.DoesNotExist, ImproperlyConfigured):
        user = AnonymousProfile()
    return user

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_profile(request)
        return request._cached_user

class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Turbion profile authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.__class__.user = LazyUser()

        return None
