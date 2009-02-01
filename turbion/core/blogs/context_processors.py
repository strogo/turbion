from django.conf import settings

def blog_globals(request):
    return {
        "blog": {
            "name": settings.TURBION_BLOG_NAME
        }
    }
