# -*- coding: utf-8 -*-
import xmlrpclib
import re

from django.conf import settings
from django.contrib.sites.models import Site
from turbion.utils.descriptor import to_descriptor

from turbion.utils.urlfetch import fetch

class ServerProxy(xmlrpclib.ServerProxy):
    pass

def search_link(content):
    match = re.search(r'<link rel="pingback" href="([^"]+)" ?/?>', content)
    return match and match.group(1)

def get_class(path):
    if isinstance(path, basestring):
        module, name = path.rsplit(".", 1)
        mod = __import__(module, {}, {}, [""])
        return getattr(mod, name)
    return path

def get_rpc_gateway(target_uri):
    try:
        response = fetch(target_uri)
        return response.headers.get('X-Pingback', '') or search_link(response.content[:512 * 1024])
    except (IOError, ValueError), e:
        return None

def call_ping(gateway, source_uri, target_uri):
    try:
        server = ServerProxy(gateway)
        q = server.pingback.ping(source_uri, target_uri)
        return q
    except xmlrpclib.Fault, e:
        return str(e)

def process_for_pingback(sender, instance, url, text, **kwargs):
    from turbion.pingback.models import Outgoing
    from turbion.pingback import utils

    domain = Site.objects.get_current().domain

    dscr = to_descriptor(sender)

    local_uri = 'http://%s%s' % (domain, url)

    for target_url in utils.parse_html_links(text, domain):
        try:
            Outgoing.objects.get(
                        target_uri=target_url,
                        descriptor=dscr,
                        object_id=instance.id,
                        status=True
                )
            continue# do nothing if we just have pinged this url from this instance of model
        except Outgoing.DoesNotExist:
            pass

        try:
            #make ping client
            gateway = get_rpc_gateway(target_url)

            if not gateway:
                continue

            status = call_ping(gateway, local_uri, target_url)
        except Exception, e:
            status = str( e )
            gateway = None

        out = Outgoing.objects.create(
                            descriptor=dscr,
                            object_id=instance.id,
                            target_uri=target_url,
                            rpcserver=gateway,
                            status=status
                    )
