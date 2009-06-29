from django.conf import settings
from django.db import models

class Blog(object):
    def __init__(self, request):
        pass

    name = settings.TURBION_BLOG_NAME

    @models.permalink
    def get_absolute_url(self):
        return ("turbion_blog_index",)

def blog_globals(request):
    return {
        "blog":  Blog(request)
    }
