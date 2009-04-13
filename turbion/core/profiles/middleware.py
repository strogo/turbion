from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend

from turbion.core.profiles.models import Profile

class AnonymousProfile(AnonymousUser):
    nickname = None
    ip = None
    is_confirmed = False
    trusted = False
    site = None
    name_view = None
    site_view = None

    def is_authenticated_confirmed(self):
        return False

def get_profile(request):
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        if user:
            user = user.profile
        else:
            user = AnonymousProfile()
    except KeyError:
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
