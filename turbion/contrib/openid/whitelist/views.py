from django import http

from turbion.core.utils.compat.mimeparse import best_match
from turbion.contrib.openid.whitelist.serializers import get_accept, get_generator

def whitelist(request, queryset):
    if hasattr(queryset, '_clone'):
        queryset = queryset._clone()
    openids = list(queryset)

    accept = request.META.get('HTTP_ACCEPT', '')
    try:
        mimetype = best_match(get_accept(), accept)
    except ValueError:
        mimetype = 'text/plain'

    generator, mimetype = get_generator(mimetype)
    if generator:
        response = http.HttpResponse(mimetype=mimetype)
        generator(openids, response)
        return response

    return http.HttpResponse(
        'Can accept only: %s' % ', '.join(get_accept()),
        status=406
    )
