from django import http

from turbion.core.utils.compat.mimeparse import best_match

def whitelist(request, queryset):
    if hasattr(queryset, '_clone'):
        queryset = queryset._clone()
    openids = list(queryset)


    MIMETYPES = ['application/xml', 'text/xml', 'application/json', 'text/plain']
    accept = request.META.get('HTTP_ACCEPT', '')
    try:
        mimetype = best_match(MIMETYPES, accept)
    except ValueError:
        mimetype = 'text/plain'
    if mimetype.endswith('/xml'):
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import elementtree.ElementTree as ET
        root = ET.Element('whitelist')
        for openid in openids:
            ET.SubElement(root, 'openid').text = openid
        xml = ET.ElementTree(root)
        response = http.HttpResponse(mimetype=mimetype)
        xml.write(response, encoding='utf-8')
        return response
    if mimetype == 'application/json':
        from django.utils import simplejson
        response = http.HttpResponse(mimetype=mimetype)
        simplejson.dump(list(openids), response)
        return response
    if mimetype == 'text/plain':
        return http.HttpResponse((o + '\n' for o in openids), mimetype=mimetype)

    return http.HttpResponse(
        'Can accept only: %s' % ', '.join(MIMETYPES),
        status_code = 406
    )
