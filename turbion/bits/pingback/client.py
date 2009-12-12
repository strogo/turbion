import xmlrpclib
import re

from django.conf import settings
from django.contrib.sites.models import Site

from turbion import logger
from turbion.bits.utils.urlfetch import fetch

class ServerProxy(xmlrpclib.ServerProxy):
    pass

def search_link(content):
    match = re.search(r'<link rel="pingback" href="([^"]+)" ?/?>', content)
    return match and match.group(1)

def get_rpc_gateway(target_uri):
    try:
        response = fetch(target_uri)
        return response.headers.get('X-Pingback', '') or search_link(response.content[:512 * 1024])
    except (IOError, ValueError), e:
        return None

def ping_links(instance, **kwargs):
    from turbion.bits.pingback.models import Pingback
    from turbion.bits.pingback import utils

    domain = Site.objects.get_current().domain

    local_url = 'http://%s%s' % (domain, instance.get_absolute_url())

    for target_url in utils.parse_html_links(instance.text_html, domain):
        try:
            Pingback.objects.get(
                target_url=target_url,
                source_url=local_url,
                post=None,
                finished=True,
                incoming=False
            )
            continue# do nothing if we just have pinged this url from this instance of model
        except Pingback.DoesNotExist:
            pass

        try:
            gateway = get_rpc_gateway(target_url)
        except Exception, e:
            logger.warning(str(e))
            continue

        if not gateway:
            continue

        try:
            server = ServerProxy(gateway)
            status = server.pingback.ping(local_url, target_url)
        except Exception, e:
            logger.warning(str(e))
            continue

        try:
            code = int(status)
            status = utils.get_code_description(code)
        except (TypeError, ValueError):
            code = None

        out = Pingback.objects.create(
            post=None,
            target_url=target_url,
            source_url=local_url,
            status=status,
            finished=code is None
        )
